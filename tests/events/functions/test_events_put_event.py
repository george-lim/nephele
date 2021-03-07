import json
import os

import pytest
import src
from src.events.functions.put_event import handler


@pytest.mark.parametrize(
    "command, exception_message, expected_out",
    [
        ("/putevent '", "No closing quotation", "Failed to parse input."),
        (
            "/putevent",
            "missing event details",
            "Please provide an event name, cron expression, and command to put.",
        ),
    ],
)
def test_put_event_user_error(capsys, command, exception_message, expected_out):
    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": command,
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == exception_message

    out, err = capsys.readouterr()

    assert out.strip() == expected_out
    assert err.strip() == ""


def test_put_event(capsys, mock_aws_events):
    user_id = "telegram_000000000"
    event_name = "event"

    resource_prefix = os.environ["RESOURCE_PREFIX"]
    namespace = f"{resource_prefix}-{user_id}"
    expected_rule_name = f"{namespace}-{event_name}"

    expected_rule = {
        "Arn": f"arn:aws:events:us-east-1:111111111111:rule/{expected_rule_name}",
        "EventBusName": "default",
        "Name": expected_rule_name,
        "ScheduleExpression": "cron(* * ? * * *)",
        "State": "ENABLED",
    }

    expected_target_input = {
        "command": "hello world!",
        "interface": {"name": "telegram", "chat_id": "000000000"},
        "user_id": user_id,
    }

    expected_target = {
        "Id": f"{expected_rule_name}-target",
        "Arn": "arn:aws:states:::stateMachine:TelegramRequest",
        "RoleArn": os.environ["TARGET_ROLE_ARN"],
        "Input": json.dumps(expected_target_input),
    }

    handler(
        {
            "command": f"/putevent {event_name} '* * ? * * *' hello world!",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    response = mock_aws_events.list_rules(NamePrefix=namespace)

    assert len(response["Rules"]) == 1
    assert response["Rules"][0] == expected_rule

    response = mock_aws_events.list_targets_by_rule(Rule=expected_rule_name)

    assert len(response["Targets"]) == 1
    assert response["Targets"][0] == expected_target

    out, err = capsys.readouterr()

    assert out.strip() == "Successfully put event!"
    assert err.strip() == ""


def test_put_event_exception(capsys, monkeypatch):
    def put_event(self, event_name, cron_expression, target_arn, event):
        raise Exception("put event failed")

    monkeypatch.setattr(src.events.scheduler.Scheduler, "put_event", put_event)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/putevent event '* * ? * * *' hello world!",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "put event failed"

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to put event."
    assert err.strip() == ""
