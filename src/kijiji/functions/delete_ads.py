from src.core.interface import Interface
from src.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event["user_id"])
        kijiji_ad_archive_bucket.delete_archive()

        interface.reply_message("Successfully deleted Kijiji ad archive!")
    except Exception:
        interface.reply_message("Failed to delete Kijiji ad archive.")
        raise
