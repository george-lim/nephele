import json
import os

import pytest
import src
from src.events.functions.list_events import handler


@pytest.mark.parametrize("has_existing_rules", [True, False])
def test_list_events(capsys, mock_aws_events, has_existing_rules):
    user_id = "telegram_000000000"

    event = {
        "command": "/listevents",
        "interface": {"name": "telegram", "chat_id": "000000000"},
        "user_id": user_id,
    }

    if has_existing_rules:
        rule_count = 5
        resource_prefix = os.environ["RESOURCE_PREFIX"]
        namespace = f"{resource_prefix}-{user_id}"

        for i in range(0, rule_count):
            rule_name = f"{namespace}-event{i}"

            targets = [
                {
                    "Id": f"{rule_name}-target",
                    "Arn": "arn:aws:states:::stateMachine:TelegramRequest",
                    "RoleArn": os.environ["TARGET_ROLE_ARN"],
                    "Input": json.dumps(event),
                }
            ]

            mock_aws_events.put_rule(
                Name=rule_name, ScheduleExpression="cron(* * ? * * *)", State="DISABLED"
            )

            mock_aws_events.put_targets(Rule=rule_name, Targets=targets)

    handler(event)

    out, err = capsys.readouterr()

    if has_existing_rules:
        expected_out = "\n".join(
            [
                f"""Name: event{i}
State: DISABLED
Cron Expression: * * ? * * *
Command: /listevents"""
                for i in range(0, rule_count)
            ]
        )

        assert out.strip() == expected_out
    else:
        assert out.strip() == "No events found!"

    assert err.strip() == ""


def test_list_events_exception(capsys, monkeypatch):
    def list_events(self):
        raise Exception("list events failed")

    monkeypatch.setattr(src.events.scheduler.Scheduler, "list_events", list_events)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/listevents",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "list events failed"

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to list events."
    assert err.strip() == ""
