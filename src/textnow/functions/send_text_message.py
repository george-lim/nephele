import json
import shlex

from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface
from src.core.sync_playwright import Playwright
from textnow_bot import TextNowBot


def handler(event, context=None):
    interface = Interface(event["interface"])
    playwright = Playwright(event["user_id"])

    users_table = UsersTable(event["user_id"])
    cookies = json.loads(users_table.user.get("cookies", "null"))

    try:
        args = shlex.split(event["command"])[1:]
    except Exception:
        interface.reply_message("Failed to parse input.")
        raise

    if len(args) < 2:
        interface.reply_message(
            "Please provide a recipient and message to send on TextNow."
        )

        raise Exception("missing message details")

    if cookies is None:
        interface.reply_message("Please log into TextNow first.")
        raise Exception("authentication failed")

    interface.reply_message("Sending text message on TextNow...")

    try:
        recipient = args[0]
        message = " ".join(args[1:])

        def bot(page):
            bot = TextNowBot(page)

            bot.log_in(cookies)
            bot.send_text_message(recipient, message)

        playwright.execute(bot)

        interface.reply_message("Successfully sent text message on TextNow!")
    except Exception:
        if playwright.screenshot_path.exists():
            interface.reply_photo(playwright.screenshot_path)
        else:
            interface.reply_message("Failed to send text message on TextNow.")

        raise
