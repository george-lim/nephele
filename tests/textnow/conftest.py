import os

import pytest
import textnow_bot


@pytest.fixture(autouse=True)
def add_service_name(monkeypatch):
    monkeypatch.setitem(os.environ, "SERVICE_NAME", "textnow")


@pytest.fixture(autouse=True)
def mock_textnow_bot(monkeypatch):
    @property
    def cookies(self):
        return [
            {
                "name": "PermissionPriming",
                "value": "-1",
                "domain": "www.textnow.com",
                "path": "/",
                "expires": -1,
                "httpOnly": False,
                "secure": True,
                "sameSite": "None",
            }
        ]

    monkeypatch.setattr(
        textnow_bot.TextNowBot, "__init__", lambda *args, **kwargs: None
    )

    monkeypatch.setattr(textnow_bot.TextNowBot, "cookies", cookies)

    monkeypatch.setattr(textnow_bot.TextNowBot, "log_in", lambda *args, **kwargs: None)

    monkeypatch.setattr(
        textnow_bot.TextNowBot, "send_text_message", lambda *args, **kwargs: None
    )
