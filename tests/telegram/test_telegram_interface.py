from pathlib import Path

import pytest


def test_getter_functions(mock_telegram_interface):
    assert mock_telegram_interface.get_name() == "telegram"

    assert (
        mock_telegram_interface.get_request_arn()
        == "arn:aws:states:::stateMachine:TelegramRequest"
    )


def test_reply_document(mock_telegram_interface):
    document_path = Path("/tmp/test_document.txt")
    document_path.write_text("hello world!")

    response = mock_telegram_interface.reply_document(document_path)

    assert response.url == "https://api.telegram.org/bot/sendDocument"
    assert response.data == {"chat_id": "000000000"}

    assert response.files == {
        "document": (document_path.name, document_path.read_bytes())
    }


@pytest.mark.parametrize(
    "message, parse_mode", [("hello world!", None), (r"hello world\!", "MarkdownV2")]
)
def test_reply_message(mock_telegram_interface, message, parse_mode):
    response = mock_telegram_interface.reply_message(message, parse_mode)

    data = {"chat_id": "000000000", "text": message}

    if parse_mode is not None:
        data["parse_mode"] = parse_mode

    assert response.url == "https://api.telegram.org/bot/sendMessage"
    assert response.data == data
    assert response.files is None


def test_reply_photo(mock_telegram_interface):
    photo_path = Path("/tmp/test_photo.png")
    photo_path.write_text("hello world!")

    response = mock_telegram_interface.reply_photo(photo_path)

    assert response.url == "https://api.telegram.org/bot/sendPhoto"
    assert response.data == {"chat_id": "000000000"}
    assert response.files == {"photo": (photo_path.name, photo_path.read_bytes())}
