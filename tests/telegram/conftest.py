import os

import pytest
import requests
from src.telegram.interface import TelegramInterface


@pytest.fixture
def mock_telegram_interface(monkeypatch):
    monkeypatch.setitem(os.environ, "TELEGRAM_INTERFACE_NAME", "telegram")

    monkeypatch.setitem(
        os.environ,
        "TELEGRAM_REQUEST_ARN",
        "arn:aws:states:::stateMachine:TelegramRequest",
    )

    monkeypatch.setitem(
        os.environ, "TELEGRAM_REQUEST_BASE_URL", "https://api.telegram.org/bot"
    )

    class Response:
        def __init__(self, url, data, files=None):
            self._url = url
            self._data = data
            self._files = files

        @property
        def url(self):
            return self._url

        @property
        def data(self):
            return self._data

        @property
        def files(self):
            return self._files

        def raise_for_status(self):
            pass

    class Session:
        def post(self, url, data, files=None):
            return Response(url, data, files)

    monkeypatch.setattr(requests, "Session", Session)

    return TelegramInterface({"name": "telegram", "chat_id": "000000000"})
