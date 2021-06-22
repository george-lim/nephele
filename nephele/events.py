import json
import os

import boto3


class Events:
    def __init__(self, event):
        self._client = boto3.client("events")
        self._target_arn = os.environ["eventsTargetArn"]
        self._namespace = event["namespace"]
        self._target_id = "1"

    @property
    def ResourceNotFoundException(self):
        return self._client.exceptions.ResourceNotFoundException

    def describe_rule(self, name):
        name = f"{self._namespace}-{name}"
        rule = self._client.describe_rule(Name=name)

        # Truncate 'cron(' prefix and ')' suffix
        cron_expression = rule["ScheduleExpression"][5:-1]

        targets_paginator = self._client.get_paginator("list_targets_by_rule")

        for page in targets_paginator.paginate(Rule=name):
            first_target = page["Targets"][0]
            event = json.loads(first_target["Input"])
            break

        return {"event": event, "cron_expression": cron_expression}

    def put_rule(self, name, event, cron_expression):
        name = f"{self._namespace}-{name}"
        schedule_expression = f"cron({cron_expression})"
        self._client.put_rule(Name=name, ScheduleExpression=schedule_expression)

        targets = [
            {
                "Id": self._target_id,
                "Arn": self._target_arn,
                "Input": json.dumps(event),
            }
        ]

        self._client.put_targets(Rule=name, Targets=targets)

    def delete_rule(self, name):
        name = f"{self._namespace}-{name}"
        self._client.remove_targets(Rule=name, Ids=[self._target_id])
        self._client.delete_rule(Name=name)
