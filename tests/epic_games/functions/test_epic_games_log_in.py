import json

import pytest
from src.core.dynamodb.users_table import UsersTable
from src.epic_games.functions.log_in import handler


def test_log_in(capsys, mock_users_table, mock_sync_playwright):
    user_id = "telegram_000000000"

    cookies_str = json.dumps(
        [
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
    )

    expected_user = {"cookies": cookies_str}

    users_table = UsersTable(user_id)

    handler(
        {
            "command": "/loginepicgames username password",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    assert users_table.user == expected_user

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Logging into Epic Games...
Successfully logged into Epic Games!"""
    )

    assert err.strip() == ""


@pytest.mark.parametrize(
    "mock_sync_playwright_exception, command, exception_message, expected_out",
    [
        (True, "/loginepicgames '", "No closing quotation", "Failed to parse input."),
        (
            True,
            "/loginepicgames",
            "missing account credentials",
            "Please provide an account username and password to log into Epic Games.",
        ),
        (
            True,
            "/loginepicgames username password",
            "bot execution failed with screenshot",
            """Logging into Epic Games...
b'playwright screenshot'""",
        ),
        (
            False,
            "/loginepicgames username password",
            "bot execution failed without screenshot",
            """Logging into Epic Games...
Failed to log into Epic Games.""",
        ),
    ],
    indirect=["mock_sync_playwright_exception"],
)
def test_log_in_exception(
    capsys, mock_sync_playwright_exception, command, exception_message, expected_out
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
