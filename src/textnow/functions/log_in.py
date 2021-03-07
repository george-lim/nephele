import json
import shlex

from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface
from src.core.sync_playwright import Playwright
from textnow_bot import TextNowBot


def handler(event, context=None):
    interface = Interface(event["interface"])
    playwright = Playwright(event["user_id"])

    try:
        args = shlex.split(event["command"])[1:]
    except Exception:
        interface.reply_message("Failed to parse input.")
        raise

    if len(args) < 2:
        interface.reply_message(
            "Please provide an account username and password to log into TextNow."
        )

        raise Exception("missing account credentials")

    interface.reply_message("Logging into TextNow...")

    try:
        [username, password] = [*args]

        def bot(page):
            bot = TextNowBot(page)

            bot.log_in(None, username, password)
            return bot.cookies

        cookies = playwright.execute(bot)

        interface.reply_message("Successfully logged into TextNow!")

        users_table = UsersTable(event["user_id"])
        users_table.user = {"cookies": json.dumps(cookies)}
    except Exception:
        if playwright.screenshot_path.exists():
            interface.reply_photo(playwright.screenshot_path)
        else:
            interface.reply_message("Failed to log into TextNow.")

        raise
