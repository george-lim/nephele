import os

import boto3
import pytest
from moto import mock_s3


@pytest.fixture(autouse=True)
def add_service_name(monkeypatch):
    monkeypatch.setitem(os.environ, "SERVICE_NAME", "kijiji")


@pytest.fixture(autouse=True)
def mock_kijiji_ad_archive_bucket(monkeypatch):
    monkeypatch.setitem(
        os.environ, "KIJIJI_AD_ARCHIVE_BUCKET_NAME", "nephele-dev-kijijiadarchivebucket"
    )

    with mock_s3():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=os.environ["KIJIJI_AD_ARCHIVE_BUCKET_NAME"])

        yield s3
