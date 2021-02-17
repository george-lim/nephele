from lib.core.interface import Interface
from lib.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket

def handler(event, _):
  interface = Interface(event['interface'])
  kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event['userId'])

  try:
    presigned_post_path = kijiji_ad_archive_bucket.generate_presigned_post()

    interface.reply_message('''Please upload an archive of Kijiji ads with the following form data:

  Restrictions:
  1. Ad archive must not exceed 25 MB
  2. Form expires after 5 minutes''')

    interface.reply_document(presigned_post_path)
  except:
    interface.reply_message('Failed to generate upload form data')
    raise
