import boto3
import json
import pathlib
import zipfile

_ARCHIVE_PATH = pathlib.Path('/tmp/s3_archive.zip')

_s3 = boto3.client('s3')

def delete_object(bucket_name, key):
  return _s3.delete_object(Bucket=bucket_name, Key=key)

def download_file(bucket_name, key, file_path):
  return _s3.download_file(bucket_name, key, str(file_path))

def download_archive(bucket_name, key, extract_path):
  download_file(bucket_name, key, _ARCHIVE_PATH)

  with zipfile.ZipFile(_ARCHIVE_PATH, 'r') as archive:
    extract_path.mkdir(parents=True, exist_ok=True)
    archive.extractall(extract_path)

def generate_presigned_post(bucket_name, key, conditions, expiration, presigned_post_path):
  with open(presigned_post_path, 'w') as file:
    response = _s3.generate_presigned_post(bucket_name, key, Conditions=conditions, ExpiresIn=expiration)
    json.dump(response, file)
