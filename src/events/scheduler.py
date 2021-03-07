import json
import os

import boto3


class Scheduler:
    def __init__(self, user_id):
        self.events = boto3.client("events")

        resource_prefix = os.environ["RESOURCE_PREFIX"]
        self.namespace = f"{resource_prefix}-{user_id}"

        self.target_role_arn = os.environ.get("TARGET_ROLE_ARN")

    def get_rule_info(self, event_name):
        return {
            "name": f"{self.namespace}-{event_name}",
            "target_id": f"{self.namespace}-{event_name}-target",
        }

    def delete_event(self, event_name):
        rule_info = self.get_rule_info(event_name)

        self.events.remove_targets(Rule=rule_info["name"], Ids=[rule_info["target_id"]])
        self.events.delete_rule(Name=rule_info["name"])

    def disable_event(self, event_name):
        rule_info = self.get_rule_info(event_name)
        self.events.disable_rule(Name=rule_info["name"])

    def enable_event(self, event_name):
        rule_info = self.get_rule_info(event_name)
        self.events.enable_rule(Name=rule_info["name"])

    def list_events(self):
        events = []

        rule_name_start_index = len(self.namespace) + 1
        cron_expression_start_index = len("cron(")
        cron_expression_end_index = -len(")")

        rules_paginator = self.events.get_paginator("list_rules")
        rules_iterator = rules_paginator.paginate(NamePrefix=self.namespace)

        for rules_page in rules_iterator:
            for rule in rules_page["Rules"]:
                targets_paginator = self.events.get_paginator("list_targets_by_rule")
                targets_iterator = targets_paginator.paginate(Rule=rule["Name"])

                for targets_page in targets_iterator:
                    target = targets_page["Targets"][0]
                    break

                events.append(
                    {
                        "name": rule["Name"][rule_name_start_index:],
                        "state": rule["State"],
                        "cron_expression": rule["ScheduleExpression"][
                            cron_expression_start_index:cron_expression_end_index
                        ],
                        "command": json.loads(target["Input"])["command"],
                    }
                )

        return events

    def put_event(self, event_name, cron_expression, target_arn, event):
        rule_info = self.get_rule_info(event_name)
        schedule_expression = f"cron({cron_expression})"

        targets = [
            {
                "Id": rule_info["target_id"],
                "Arn": target_arn,
                "RoleArn": self.target_role_arn,
                "Input": json.dumps(event),
            }
        ]

        self.events.put_rule(
            Name=rule_info["name"], ScheduleExpression=schedule_expression
        )

        self.events.put_targets(Rule=rule_info["name"], Targets=targets)
