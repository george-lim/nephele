import json

import pytest
from src.core.dynamodb.users_table import UsersTable
from src.textnow.functions.log_in import handler


def test_log_in(capsys, mock_users_table, mock_sync_playwright):
    user_id = "telegram_000000000"

    cookies_str = json.dumps(
        [
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
    )

    expected_user = {"cookies": cookies_str}

    users_table = UsersTable(user_id)

    handler(
        {
            "command": "/logintextnow username password",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    assert users_table.user == expected_user

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Logging into TextNow...
Successfully logged into TextNow!"""
    )

    assert err.strip() == ""


@pytest.mark.parametrize(
    "mock_sync_playwright_exception, command, exception_message, expected_out",
    [
        (True, "/logintextnow '", "No closing quotation", "Failed to parse input."),
        (
            True,
            "/logintextnow",
            "missing account credentials",
            "Please provide an account username and password to log into TextNow.",
        ),
        (
            True,
            "/logintextnow username password",
            "bot execution failed with screenshot",
            """Logging into TextNow...
b'playwright screenshot'""",
        ),
        (
            False,
            "/logintextnow username password",
            "bot execution failed without screenshot",
            """Logging into TextNow...
Failed to log into TextNow.""",
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
