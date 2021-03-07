import pytest
from src.core.dynamodb.users_table import UsersTable
from src.textnow.functions.send_text_message import handler


@pytest.mark.parametrize(
    "command, exception_message, expected_out",
    [
        ("/sendtextmessage '", "No closing quotation", "Failed to parse input."),
        (
            "/sendtextmessage",
            "missing message details",
            "Please provide a recipient and message to send on TextNow.",
        ),
        (
            "/sendtextmessage 0000000000 hello world!",
            "authentication failed",
            "Please log into TextNow first.",
        ),
    ],
)
def test_send_text_message_user_error(
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


def test_send_text_message(capsys, mock_users_table, mock_sync_playwright):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"cookies": "[{}]"}

    handler(
        {
            "command": "/sendtextmessage 0000000000 hello world!",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Sending text message on TextNow...
Successfully sent text message on TextNow!"""
    )

    assert err.strip() == ""


@pytest.mark.parametrize(
    "mock_sync_playwright_exception, exception_message, expected_out",
    [
        (
            True,
            "bot execution failed with screenshot",
            """Sending text message on TextNow...
b'playwright screenshot'""",
        ),
        (
            False,
            "bot execution failed without screenshot",
            """Sending text message on TextNow...
Failed to send text message on TextNow.""",
        ),
    ],
    indirect=["mock_sync_playwright_exception"],
)
def test_send_text_message_exception(
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
                "command": "/sendtextmessage 0000000000 hello world!",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": user_id,
            }
        )

    assert str(exception_info.value) == exception_message

    out, err = capsys.readouterr()

    assert out.strip() == expected_out
    assert err.strip() == ""
