import os
import pathlib
from src.common.actions import reply_document, reply_message
from src.common.s3 import download_file

_ARCHIVE_PATH = pathlib.Path('/tmp/kijiji_ads.zip')
_KIJIJI_ADS_BUCKET_NAME = os.environ.get('KIJIJI_ADS_BUCKET_NAME')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']

  try:
    download_file(_KIJIJI_ADS_BUCKET_NAME, user_id, _ARCHIVE_PATH)
  except:
    reply_message(interface, 'Failed to download ads.')
    raise

  reply_document(interface, _ARCHIVE_PATH)
