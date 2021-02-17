from lib.core.interface import Interface
from lib.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket

def handler(event, _):
  interface = Interface(event['interface'])

  try:
    kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event['userId'])
    archive_path = kijiji_ad_archive_bucket.download_archive()

    interface.reply_document(archive_path)
  except:
    interface.reply_message('Failed to download Kijiji ads: archive not found.')
    raise
