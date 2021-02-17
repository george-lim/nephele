import boto3
import json
import os
import pathlib
import shutil
import zipfile

_KIJIJI_AD_ARCHIVE_BUCKET_NAME = os.environ.get('KIJIJI_AD_ARCHIVE_BUCKET_NAME')

_MAX_UPLOAD_SIZE_CONDITION = ['content-length-range', 0, 26214400]
_PRESIGNED_POST_EXPIRATION_SECONDS = 300

_s3 = boto3.client('s3')

class KijijiAdArchiveBucket:
  def __init__(self, user_id):
    self.key = user_id

    self.kijiji_ad_archive_path = pathlib.Path(f'/tmp/{user_id}/kijiji_ad_archive.zip')
    self.presigned_post_path = pathlib.Path(f'/tmp/{user_id}/presigned_post.json')

    self.ads_path = self.kijiji_ad_archive_path.with_suffix('').joinpath(user_id)

  def delete_archive(self):
    _s3.delete_object(Bucket=_KIJIJI_AD_ARCHIVE_BUCKET_NAME, Key=self.key)

  def download_archive(self):
    self.kijiji_ad_archive_path.parent.mkdir(0o755, True, True)

    _s3.download_file(_KIJIJI_AD_ARCHIVE_BUCKET_NAME, self.key, str(self.kijiji_ad_archive_path))

    return self.kijiji_ad_archive_path

  def extract_archive(self):
    if self.ads_path.exists():
      shutil.rmtree(self.ads_path)

    self.ads_path.mkdir(0o755, True)

    with zipfile.ZipFile(self.kijiji_ad_archive_path) as archive:
      archive.extractall(self.ads_path)

    return self.ads_path

  def generate_presigned_post(self):
    response = _s3.generate_presigned_post(
      _KIJIJI_AD_ARCHIVE_BUCKET_NAME,
      self.key,
      None,
      [_MAX_UPLOAD_SIZE_CONDITION],
      _PRESIGNED_POST_EXPIRATION_SECONDS
    )

    self.presigned_post_path.parent.mkdir(0o755, True, True)
    self.presigned_post_path.write_text(json.dumps(response))
    return self.presigned_post_path
