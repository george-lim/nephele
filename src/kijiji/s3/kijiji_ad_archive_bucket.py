import json
import os
from pathlib import Path
from shutil import rmtree
from time import strftime
from zipfile import ZipFile

import boto3


class KijijiAdArchiveBucket:
    def __init__(self, user_id):
        self.max_upload_size_condition = ["content-length-range", 0, 26214400]
        self.presigned_post_expiration_seconds = 300

        self.s3 = boto3.client("s3")
        self.bucket_name = os.environ["KIJIJI_AD_ARCHIVE_BUCKET_NAME"]
        self.key = user_id

        self._kijiji_ad_archive_path = Path(
            f"/tmp/kijiji_ad_archive_{user_id}_{strftime('%Y%m%dT%H%M%S')}.zip"
        )

        self._presigned_post_path = Path(
            f"/tmp/presigned_post_{user_id}_{strftime('%Y%m%dT%H%M%S')}.json"
        )

    @property
    def kijiji_ad_archive_path(self):
        return self._kijiji_ad_archive_path

    @property
    def presigned_post_path(self):
        return self._presigned_post_path

    @property
    def ads_path(self):
        return self.kijiji_ad_archive_path.with_suffix("")

    def delete_archive(self):
        self.s3.delete_object(Bucket=self.bucket_name, Key=self.key)

    def download_archive(self):
        self.s3.download_file(
            self.bucket_name, self.key, str(self.kijiji_ad_archive_path)
        )

    def extract_archive(self):
        if self.ads_path.exists():
            rmtree(self.ads_path)

        self.ads_path.mkdir(0o755, True)

        with ZipFile(self.kijiji_ad_archive_path) as archive:
            archive.extractall(self.ads_path)

    def generate_presigned_post(self):
        response = self.s3.generate_presigned_post(
            self.bucket_name,
            self.key,
            None,
            [self.max_upload_size_condition],
            self.presigned_post_expiration_seconds,
        )

        self.presigned_post_path.write_text(json.dumps(response))
