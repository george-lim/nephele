import os
import pathlib
from src.common.actions import reply_document, reply_message
from src.common.s3 import generate_presigned_post

_KIJIJI_SERVICE_NAME = os.environ.get('KIJIJI_SERVICE_NAME')
_KIJIJI_ADS_BUCKET_NAME = os.environ.get('KIJIJI_ADS_BUCKET_NAME')
_PRESIGNED_POST_PATH = pathlib.Path('/tmp/presigned_post.json')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']

  if event['serviceName'] == _KIJIJI_SERVICE_NAME:
    conditions = [['content-length-range', 0, 26214400]]
    generate_presigned_post(_KIJIJI_ADS_BUCKET_NAME, user_id, conditions, 300, _PRESIGNED_POST_PATH)
    reply_message(interface, 'Reminder: There is a 25 MB file size limit for Kijiji ads archive uploads. Server access expires in 5 minutes.')
  else:
    raise Exception('Unknown service name')

  reply_message(interface, 'Please make a POST request with the following form fields to upload your file:')
  reply_document(interface, _PRESIGNED_POST_PATH)
