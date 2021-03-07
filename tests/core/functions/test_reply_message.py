import pytest
from src.core.functions.reply_message import handler


@pytest.mark.parametrize(
    "interface", [{"name": "telegram", "chat_id": "000000000"}],
)
@pytest.mark.parametrize(
    "message, parse_mode", [("hello world!", None), (r"hello world\!", "MarkdownV2")]
)
def test_reply_message(capsys, interface, message, parse_mode):
    handler({"interface": interface, "message": message, "parseMode": parse_mode})

    out, err = capsys.readouterr()

    assert out.strip() == message
    assert err.strip() == ""


def test_reply_message_invalid_interface():
    with pytest.raises(Exception) as exception_info:
        handler({"interface": {"name": ""}, "message": "hello world!"})

    assert str(exception_info.value) == "invalid interface name"
