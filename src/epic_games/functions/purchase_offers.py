import json

from epic_games_bot import EpicGamesBot
from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface
from src.core.sync_playwright import Playwright


def handler(event, context=None):
    interface = Interface(event["interface"])
    playwright = Playwright(event["user_id"])

    users_table = UsersTable(event["user_id"])
    cookies = json.loads(users_table.user.get("cookies", "null"))

    if cookies is None:
        interface.reply_message("Please log into Epic Games first.")
        raise Exception("authentication failed")

    interface.reply_message("Purchasing free promotional offers on Epic Games...")

    try:

        def bot(page):
            bot = EpicGamesBot(page)

            bot.log_in(cookies)

            purchased_offer_urls = bot.purchase_free_promotional_offers()
            return purchased_offer_urls

        purchased_offer_urls = playwright.execute(bot)

        if len(purchased_offer_urls) == 0:
            interface.reply_message(
                "Already purchased free promotional offers on Epic Games!"
            )
        else:
            interface.reply_message(
                "Successfully purchased free promotional offers on Epic Games:"
            )

            [interface.reply_message(offer_url) for offer_url in purchased_offer_urls]
    except Exception:
        if playwright.screenshot_path.exists():
            interface.reply_photo(playwright.screenshot_path)
        else:
            interface.reply_message(
                "Failed to purchase free promotional offers on Epic Games."
            )

        raise
