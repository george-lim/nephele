import kijiji_bot
import pytest
from src.core.dynamodb.users_table import UsersTable
from src.kijiji.functions.log_in import handler


@pytest.mark.parametrize(
    "command, exception_message, expected_out",
    [
        ("/loginkijiji '", "No closing quotation", "Failed to parse input."),
        (
            "/loginkijiji",
            "missing SSID cookie value",
            r"""Please provide a SSID cookie value to log into Kijiji\. To get this value:

1\. Log into Kijiji on any browser, with `Keep me signed in` checked
2\. Using a web inspector, copy the value of the `ssid` cookie in the domain `www\.kijiji\.ca`

Ensure that you do not log out of the Kijiji session afterwards\.
If you do, you will need another SSID cookie value to authenticate again\.""",
        ),
    ],
)
def test_log_in_user_error(capsys, command, exception_message, expected_out):
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


def test_log_in(capsys, monkeypatch, mock_users_table):
    user_id = "telegram_000000000"

    expected_user = {"ssid": "MTAyMDk0ODE1Mnxl..."}

    users_table = UsersTable(user_id)

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", lambda *args, **kwargs: None)

    handler(
        {
            "command": "/loginkijiji MTAyMDk0ODE1Mnxl...",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    assert users_table.user == expected_user

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Logging into Kijiji...
Successfully logged into Kijiji!"""
    )

    assert err.strip() == ""


def test_log_in_exception(capsys, monkeypatch):
    def __init__(self, ssid):
        raise Exception("authentication failed")

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", __init__)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/loginkijiji username password",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "authentication failed"

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Logging into Kijiji...
Failed to log into Kijiji."""
    )

    assert err.strip() == ""
