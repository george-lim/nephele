import os
from src.common.actions import reply_message
from src.common.s3 import delete_object

_KIJIJI_ADS_BUCKET_NAME = os.environ.get('KIJIJI_ADS_BUCKET_NAME')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']

  try:
    delete_object(_KIJIJI_ADS_BUCKET_NAME, user_id)
  except:
    reply_message(interface, 'Failed to delete ads.')
    raise

  reply_message(interface, 'Successfully deleted ads!')
