from src.core.interface import Interface
from src.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event["user_id"])
        kijiji_ad_archive_bucket.generate_presigned_post()

        interface.reply_message(
            """Please upload an archive of Kijiji ads with the following form data:

Restrictions:
1. Ad archive must not exceed 25 MB
2. Form expires after 5 minutes"""
        )

        interface.reply_document(kijiji_ad_archive_bucket.presigned_post_path)
    except Exception:
        interface.reply_message(
            "Failed to generate upload form data for Kijiji ad archive."
        )

        raise
