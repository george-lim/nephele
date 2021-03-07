import os

import epic_games_bot
import pytest


@pytest.fixture(autouse=True)
def add_service_name(monkeypatch):
    monkeypatch.setitem(os.environ, "SERVICE_NAME", "epicGames")


@pytest.fixture(autouse=True)
def mock_epic_games_bot(monkeypatch):
    @property
    def cookies(self):
        return [
            {
                "name": "HAS_ACCEPTED_AGE_GATE_ONCE",
                "value": "true",
                "domain": "www.epicgames.com",
                "path": "/",
                "expires": -1,
                "httpOnly": False,
                "secure": False,
                "sameSite": "None",
            }
        ]

    monkeypatch.setattr(
        epic_games_bot.EpicGamesBot, "__init__", lambda *args, **kwargs: None
    )

    monkeypatch.setattr(epic_games_bot.EpicGamesBot, "cookies", cookies)

    monkeypatch.setattr(
        epic_games_bot.EpicGamesBot, "log_in", lambda *args, **kwargs: None
    )
