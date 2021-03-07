import os
from pathlib import Path
from zipfile import ZipFile

import pytest
from src.kijiji.functions.download_ads import handler


def test_download_ads(capsys, mock_kijiji_ad_archive_bucket):
    user_id = "telegram_000000000"

    kijiji_ad_archive_path = Path("/tmp/kijiji_ad_archive.zip")

    with ZipFile(kijiji_ad_archive_path, "w") as archive:
        archive.writestr("hello_world.txt", "hello world!")

    mock_kijiji_ad_archive_bucket.put_object(
        Body=kijiji_ad_archive_path.read_bytes(),
        Bucket=os.environ["KIJIJI_AD_ARCHIVE_BUCKET_NAME"],
        Key=user_id,
    )

    handler(
        {
            "command": "/downloadads",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": user_id,
        }
    )

    out, err = capsys.readouterr()

    assert out.strip() == str(kijiji_ad_archive_path.read_bytes())
    assert err.strip() == ""


def test_download_ads_exception(capsys):
    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/downloadads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert (
        str(exception_info.value)
        == "An error occurred (404) when calling the HeadObject operation: Not Found"
    )

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to download Kijiji ad archive."
    assert err.strip() == ""
