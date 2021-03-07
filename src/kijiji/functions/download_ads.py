from src.core.interface import Interface
from src.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event["user_id"])
        kijiji_ad_archive_bucket.download_archive()

        interface.reply_document(kijiji_ad_archive_bucket.kijiji_ad_archive_path)
    except Exception:
        interface.reply_message("Failed to download Kijiji ad archive.")
        raise
