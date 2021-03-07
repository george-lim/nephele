import os

import pytest
from src.kijiji.functions.delete_ads import handler


def test_delete_ads(capsys):
    handler(
        {
            "command": "/deleteads",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": "telegram_000000000",
        }
    )

    out, err = capsys.readouterr()

    assert out.strip() == "Successfully deleted Kijiji ad archive!"
    assert err.strip() == ""


def test_delete_ads_exception(capsys, monkeypatch):
    monkeypatch.setitem(
        os.environ,
        "KIJIJI_AD_ARCHIVE_BUCKET_NAME",
        "nephele-dev-kijijiadarchivebucket2",
    )

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/deleteads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value).startswith(
        "An error occurred (NoSuchBucket) when calling the DeleteObject operation"
    )

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to delete Kijiji ad archive."
    assert err.strip() == ""
