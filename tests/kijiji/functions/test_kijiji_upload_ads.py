import re

import pytest
import src
from src.kijiji.functions.upload_ads import handler


def test_upload_ads(capsys):
    handler(
        {
            "command": "/uploadads",
            "interface": {"name": "telegram", "chat_id": "000000000"},
            "user_id": "telegram_000000000",
        }
    )

    out, err = capsys.readouterr()

    assert re.match(
        r"""^Please upload an archive of Kijiji ads with the following form data:

Restrictions:
1\. Ad archive must not exceed 25 MB
2\. Form expires after 5 minutes
b'\{.+\}'$""",
        out.strip(),
    )

    assert err.strip() == ""


def test_upload_ads_exception(capsys, monkeypatch):
    def generate_presigned_post(self):
        raise Exception("generate presigned post failed")

    monkeypatch.setattr(
        src.kijiji.s3.kijiji_ad_archive_bucket.KijijiAdArchiveBucket,
        "generate_presigned_post",
        generate_presigned_post,
    )

    with pytest.raises(Exception) as exception_info:
        handler(
            {
                "command": "/uploadads",
                "interface": {"name": "telegram", "chat_id": "000000000"},
                "user_id": "telegram_000000000",
            }
        )

    assert str(exception_info.value) == "generate presigned post failed"

    out, err = capsys.readouterr()

    assert out.strip() == "Failed to generate upload form data for Kijiji ad archive."
    assert err.strip() == ""
