import os

import boto3
import pytest
from moto import mock_events


@pytest.fixture(autouse=True)
def mock_aws_events(monkeypatch):
    monkeypatch.setitem(os.environ, "AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setitem(os.environ, "RESOURCE_PREFIX", "nephele-dev-us-east-1")

    monkeypatch.setitem(
        os.environ,
        "TARGET_ROLE_ARN",
        "arn:aws:iam:::role/nephele-prod-eventsExecuteRequestRole",
    )

    with mock_events():
        events = boto3.client("events")
        yield events
