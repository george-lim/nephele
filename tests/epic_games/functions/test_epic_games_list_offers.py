import epic_games_bot
import pytest
from src.epic_games.functions.list_offers import handler


@pytest.mark.parametrize(
    "expected_offer_urls, expected_out",
    [
        (
            [
                "https://www.epicgames.com/store/en-US/product/hello/home",
                "https://www.epicgames.com/store/en-US/product/world/home",
            ],
            """https://www.epicgames.com/store/en-US/product/hello/home
https://www.epicgames.com/store/en-US/product/world/home""",
        ),
        ([], "No free promotional offers on Epic Games!"),
    ],
)
def test_list_offers(
    capsys, monkeypatch, mock_sync_playwright, expected_offer_urls, expected_out
):
    monkeypatch.setattr(
        epic_games_bot.EpicGamesBot,
        "list_free_promotional_offers",
        lambda: expected_offer_urls,
    )

    handler(
        {
            "command": "/listoffers",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": "telegram_000000000",
        }
    )

    out, err = capsys.readouterr()

    assert out.strip() == expected_out
    assert err.strip() == ""
