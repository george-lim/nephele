from kijiji_bot import KijijiBot
from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface
from src.kijiji.s3.kijiji_ad_archive_bucket import KijijiAdArchiveBucket


def handler(event, context=None):
    interface = Interface(event["interface"])

    users_table = UsersTable(event["user_id"])
    user = users_table.user

    user["is_using_alternate_ads"] = user.get("is_using_alternate_ads", False)
    user["ssid"] = user.get("ssid", "")

    try:
        bot = KijijiBot(user["ssid"])
    except Exception:
        interface.reply_message("Please log into Kijiji first.")
        raise

    try:
        kijiji_ad_archive_bucket = KijijiAdArchiveBucket(event["user_id"])
        kijiji_ad_archive_bucket.download_archive()
    except Exception:
        interface.reply_message("Failed to download Kijiji ad archive.")
        raise

    try:
        kijiji_ad_archive_bucket.extract_archive()
    except Exception:
        interface.reply_message("Failed to extract ads from Kijiji ad archive.")
        raise

    interface.reply_message("Reposting ads on Kijiji...")

    try:
        bot.repost_ads(
            kijiji_ad_archive_bucket.ads_path, user["is_using_alternate_ads"], 0
        )

        user["is_using_alternate_ads"] = not user["is_using_alternate_ads"]

        interface.reply_message("Successfully reposted Kijiji ads!")

        users_table.user = user
    except Exception:
        interface.reply_message("Failed to repost one or more Kijiji ads.")
        raise
