import epic_games_bot
import pytest
from src.core.dynamodb.users_table import UsersTable
from src.epic_games.functions.purchase_offers import handler


@pytest.mark.parametrize(
    "command, exception_message, expected_out",
    [
        (
            "/purchaseoffers",
            "authentication failed",
            "Please log into Epic Games first.",
        ),
    ],
)
def test_purchase_offers_user_error(
    capsys, mock_users_table, command, exception_message, expected_out
):
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


@pytest.mark.parametrize(
    "expected_purchased_offer_urls, expected_out",
    [
        (
            [
                "https://www.epicgames.com/store/en-US/product/hello/home",
                "https://www.epicgames.com/store/en-US/product/world/home",
            ],
            """Purchasing free promotional offers on Epic Games...
Successfully purchased free promotional offers on Epic Games:
https://www.epicgames.com/store/en-US/product/hello/home
https://www.epicgames.com/store/en-US/product/world/home""",
        ),
        (
            [],
            """Purchasing free promotional offers on Epic Games...
Already purchased free promotional offers on Epic Games!""",
        ),
    ],
)
def test_purchase_offers(
    capsys,
    monkeypatch,
    mock_users_table,
    mock_sync_playwright,
    expected_purchased_offer_urls,
    expected_out,
):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"cookies": "[{}]"}

    monkeypatch.setattr(
        epic_games_bot.EpicGamesBot,
        "purchase_free_promotional_offers",
        lambda self: expected_purchased_offer_urls,
    )

    handler(
        {
            "command": "/purchaseoffers",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    out, err = capsys.readouterr()

    assert out.strip() == expected_out
    assert err.strip() == ""


@pytest.mark.parametrize(
    "mock_sync_playwright_exception, exception_message, expected_out",
    [
        (
            True,
            "bot execution failed with screenshot",
            """Purchasing free promotional offers on Epic Games...
b'playwright screenshot'""",
        ),
        (
            False,
            "bot execution failed without screenshot",
            """Purchasing free promotional offers on Epic Games...
Failed to purchase free promotional offers on Epic Games.""",
        ),
    ],
    indirect=["mock_sync_playwright_exception"],
)
def test_purchase_offers_exception(
    capsys,
    mock_users_table,
    mock_sync_playwright_exception,
    exception_message,
    expected_out,
):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"cookies": "[{}]"}

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/purchaseoffers",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": user_id,
            }
        )

    assert str(exception_info.value) == exception_message

    out, err = capsys.readouterr()

    assert out.strip() == expected_out
    assert err.strip() == ""
