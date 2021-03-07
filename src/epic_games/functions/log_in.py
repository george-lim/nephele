import json
import shlex

from epic_games_bot import EpicGamesBot
from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface
from src.core.sync_playwright import Playwright


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
            "Please provide an account username and password to log into Epic Games."
        )

        raise Exception("missing account credentials")

    interface.reply_message("Logging into Epic Games...")

    try:
        [username, password] = [*args]

        def bot(page):
            bot = EpicGamesBot(page)

            bot.log_in(None, username, password)
            return bot.cookies

        cookies = playwright.execute(bot)

        interface.reply_message("Successfully logged into Epic Games!")

        users_table = UsersTable(event["user_id"])
        users_table.user = {"cookies": json.dumps(cookies)}
    except Exception:
        if playwright.screenshot_path.exists():
            interface.reply_photo(playwright.screenshot_path)
        else:
            interface.reply_message("Failed to log into Epic Games.")

        raise
