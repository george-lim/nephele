import pytest
import src
from src.core.dynamodb.users_table import UsersTable
from src.textnow.functions.log_out import handler


def test_log_out(capsys, mock_users_table):
    expected_user = {}

    user_id = "telegram_000000000"
    users_table = UsersTable(user_id)

    handler(
        {
            "command": "/logouttextnow",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    assert users_table.user == expected_user

    out, err = capsys.readouterr()

    assert out.strip() == "Successfully logged out of TextNow!"
    assert err.strip() == ""


def test_log_out_exception(capsys, monkeypatch, mock_users_table):
    def __init__(self, user_id):
        raise Exception("initialization failed")

    monkeypatch.setattr(src.core.dynamodb.users_table.UsersTable, "__init__", __init__)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/logouttextnow",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "initialization failed"

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to log out of TextNow."
    assert err.strip() == ""
