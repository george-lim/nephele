from lib.core.interface import Interface
from lib.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event['userId'])
    kijiji_ad_archive_bucket.delete_archive()

    interface.reply_message('Successfully deleted Kijiji ads!')
  except:
    interface.reply_message('Failed to delete Kijiji ads: archive not found.')
    raise
