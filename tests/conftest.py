import os

import boto3
import pytest
import src
from moto import mock_dynamodb2


@pytest.fixture
def mock_users_table(monkeypatch):
    monkeypatch.setitem(os.environ, "AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setitem(os.environ, "USERS_TABLE_NAME", "nephele-dev-usersTable")

    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.create_table(
            TableName=os.environ["USERS_TABLE_NAME"],
            AttributeDefinitions=[{"AttributeName": "userId", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "userId", "KeyType": "HASH"}],
        )

        yield table


@pytest.fixture(autouse=True)
def mock_interfaces(monkeypatch):
    def patch_interface(interface_name):
        interface_title = interface_name.title()

        class MockInterface:
            def __init__(self, interface):
                pass

            @staticmethod
            def get_name():
                return interface_name

            @staticmethod
            def get_request_arn():
                return f"arn:aws:states:::stateMachine:{interface_title}Request"

            def reply_document(self, document_path):
                print(document_path.read_bytes())

            def reply_message(self, message, parse_mode=None):
                print(message)

            def reply_photo(self, photo_path):
                print(photo_path.read_bytes())

        monkeypatch.setattr(
            src.core.interface, f"{interface_title}Interface", MockInterface
        )

    patch_interface("telegram")


@pytest.fixture
def mock_sync_playwright(monkeypatch):
    monkeypatch.setattr(
        src.core.sync_playwright.Playwright, "execute", lambda self, bot: bot(None)
    )


@pytest.fixture
def mock_sync_playwright_exception(monkeypatch, request):
    has_screenshot = request.param

    def execute(self, bot):
        if has_screenshot:
            self.screenshot_path.write_text("playwright screenshot")
            raise Exception("bot execution failed with screenshot")

        self.screenshot_path.unlink(True)
        raise Exception("bot execution failed without screenshot")

    monkeypatch.setattr(src.core.sync_playwright.Playwright, "execute", execute)
