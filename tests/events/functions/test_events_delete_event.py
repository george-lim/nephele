import json
import os

import pytest
from src.events.functions.delete_event import handler


@pytest.mark.parametrize(
    "command, exception_message, expected_out",
    [
        ("/deleteevent '", "No closing quotation", "Failed to parse input."),
        (
            "/deleteevent",
            "missing event name",
            "Please provide an event name to delete.",
        ),
    ],
)
def test_delete_event_user_error(capsys, command, exception_message, expected_out):
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


def test_delete_event(capsys, mock_aws_events):
    user_id = "telegram_000000000"
    event_name = "event"

    resource_prefix = os.environ["RESOURCE_PREFIX"]
    namespace = f"{resource_prefix}-{user_id}"
    rule_name = f"{namespace}-{event_name}"

    event = {
        "command": f"/deleteevent {event_name}",
        "interface": {"name": "telegram", "chat_id": "000000000"},
        "user_id": user_id,
    }

    targets = [
        {
            "Id": f"{rule_name}-target",
            "Arn": "arn:aws:states:::stateMachine:TelegramRequest",
            "RoleArn": os.environ["TARGET_ROLE_ARN"],
            "Input": json.dumps(event),
        }
    ]

    mock_aws_events.put_rule(Name=rule_name, ScheduleExpression="cron(* * ? * * *)")
    mock_aws_events.put_targets(Rule=rule_name, Targets=targets)

    handler(event)

    response = mock_aws_events.list_rules(NamePrefix=namespace)

    assert not response["Rules"]

    out, err = capsys.readouterr()

    assert out.strip() == "Successfully deleted event!"
    assert err.strip() == ""


def test_delete_event_exception(capsys):
    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/deleteevent event",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value).startswith(
        "An error occurred (ResourceNotFoundException) when calling the RemoveTargets operation"
    )

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to delete event."
    assert err.strip() == ""
