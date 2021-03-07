import os
from pathlib import Path
from zipfile import ZipFile

import kijiji_bot
import pytest
from src.core.dynamodb.users_table import UsersTable
from src.kijiji.functions.repost_ads import handler


def test_repost_ads_unauthenticated(capsys, monkeypatch, mock_users_table):
    def __init__(self, ssid):
        raise Exception("authentication failed")

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", __init__)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/repostads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "authentication failed"

    out, err = capsys.readouterr()

    assert out.strip() == "Please log into Kijiji first."
    assert err.strip() == ""


def test_repost_ads_missing_ad_archive(capsys, monkeypatch, mock_users_table):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"ssid": "MTAyMDk0ODE1Mnxl..."}

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", lambda *args, **kwargs: None)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/repostads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": user_id,
            }
        )

    assert (
        str(exception_info.value)
        == "An error occurred (404) when calling the HeadObject operation: Not Found"
    )

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to download Kijiji ad archive."
    assert err.strip() == ""


def test_repost_ads_corrupt_ad_archive(
    capsys, monkeypatch, mock_users_table, mock_kijiji_ad_archive_bucket
):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"ssid": "MTAyMDk0ODE1Mnxl..."}

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", lambda *args, **kwargs: None)

    mock_kijiji_ad_archive_bucket.put_object(
        Body=b"hello world!",
        Bucket=os.environ["KIJIJI_AD_ARCHIVE_BUCKET_NAME"],
        Key="telegram_000000000",
    )

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/repostads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": user_id,
            }
        )

    assert str(exception_info.value) == "File is not a zip file"

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to extract ads from Kijiji ad archive."
    assert err.strip() == ""


def add_kijiji_ad_archive(mock_kijiji_ad_archive_bucket, user_id):
    kijiji_ad_archive_path = Path("/tmp/kijiji_ad_archive.zip")

    with ZipFile(kijiji_ad_archive_path, "w") as archive:
        archive.writestr("hello_world.txt", "hello world!")

    mock_kijiji_ad_archive_bucket.put_object(
        Body=kijiji_ad_archive_path.read_bytes(),
        Bucket=os.environ["KIJIJI_AD_ARCHIVE_BUCKET_NAME"],
        Key=user_id,
    )


def test_repost_ads(
    capsys, monkeypatch, mock_users_table, mock_kijiji_ad_archive_bucket
):
    user_id = "telegram_000000000"
    ssid = "MTAyMDk0ODE1Mnxl..."

    expected_user = {"ssid": ssid, "is_using_alternate_ads": True}

    users_table = UsersTable(user_id)
    users_table.user = {"ssid": ssid}

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", lambda *args, **kwargs: None)

    monkeypatch.setattr(
        kijiji_bot.KijijiBot, "repost_ads", lambda *args, **kwargs: None
    )

    add_kijiji_ad_archive(mock_kijiji_ad_archive_bucket, user_id)

    handler(
        {
            "command": "/repostads",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    assert users_table.user == expected_user

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Reposting ads on Kijiji...
Successfully reposted Kijiji ads!"""
    )

    assert err.strip() == ""


def test_repost_ads_exception(
    capsys, monkeypatch, mock_users_table, mock_kijiji_ad_archive_bucket
):
    user_id = "telegram_000000000"

    users_table = UsersTable(user_id)
    users_table.user = {"ssid": "MTAyMDk0ODE1Mnxl..."}

    def repost_ads(self, ads_path, is_using_alternate_ads=False, post_delay_seconds=30):
        raise Exception("repost ads failed")

    monkeypatch.setattr(kijiji_bot.KijijiBot, "__init__", lambda *args, **kwargs: None)
    monkeypatch.setattr(kijiji_bot.KijijiBot, "repost_ads", repost_ads)

    add_kijiji_ad_archive(mock_kijiji_ad_archive_bucket, user_id)

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/repostads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": user_id,
            }
        )

    assert str(exception_info.value) == "repost ads failed"

    out, err = capsys.readouterr()

    assert (
        out.strip()
        == """Reposting ads on Kijiji...
Failed to repost one or more Kijiji ads."""
    )

    assert err.strip() == ""
