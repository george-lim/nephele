import kijiji_bot
import os
import pathlib
from src.common.actions import reply_message
from src.common.s3 import download_archive

_KIJIJI_ADS_BUCKET_NAME = os.environ.get('KIJIJI_ADS_BUCKET_NAME')

def handler(event, context):
  interface = event['interface']
  user = event['dynamodb']['Item']
  user['is_using_alternate_ads'] = user.get('is_using_alternate_ads', False)
  user_id = interface['userId']
  ads_path = pathlib.Path(f'/tmp/{_KIJIJI_ADS_BUCKET_NAME}/{user_id}')

  if not user.get('cookies'):
    reply_message(interface, 'Please log into Kijiji first.')
    raise Exception('Missing login cookies')

  try:
    download_archive(_KIJIJI_ADS_BUCKET_NAME, user_id, ads_path)
  except:
    reply_message(interface, 'Failed to download ads.')
    raise

  reply_message(interface, 'Reposting ads...')

  try:
    bot = kijiji_bot.KijijiBot(user['cookies'])
    user['cookies'] = bot.repost_ads(ads_path, is_using_alternate_ads=user['is_using_alternate_ads'])
    user['is_using_alternate_ads'] = not user['is_using_alternate_ads']
  except:
    reply_message(interface, 'Failed to repost ads.')
    raise

  reply_message(interface, 'Successfully reposted ads!')
  return user
