import kijiji_bot

from lib.core.dynamodb.users_table import UsersTable
from lib.core.interface import Interface
from lib.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket

def handler(event, _):
  interface = Interface(event['interface'])
  users_table = UsersTable(event['userId'])

  user = users_table.get_user()

  user['is_using_alternate_ads'] = user.get('is_using_alternate_ads', False)
  user['ssid'] = user.get('ssid', '')

  try:
    bot = kijiji_bot.KijijiBot(user['ssid'])
  except:
    interface.reply_message('Please log into Kijiji first.')
    raise

  try:
    kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event['userId'])
    kijiji_ad_archive_bucket.download_archive()
  except:
    interface.reply_message('Failed to download Kijiji ads: archive not found.')
    raise

  try:
    ads_path = kijiji_ad_archive_bucket.extract_archive()
  except:
    interface.reply_message('Failed to extract Kijiji ads: corrupt archive')
    raise

  interface.reply_message('Reposting Kijiji ads...')

  try:
    bot.repost_ads(ads_path, user['is_using_alternate_ads'], 0)

    user['is_using_alternate_ads'] = not user['is_using_alternate_ads']

    users_table.update_user(user)

    interface.reply_message('Successfully reposted Kijiji ads!')
  except:
    interface.reply_message('Failed to repost one or more Kijiji ads.')
    raise
