import shlex

from kijiji_bot import KijijiBot
from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        args = shlex.split(event["command"])[1:]
    except Exception:
        interface.reply_message("Failed to parse input.")
        raise

    if len(args) < 1:
        interface.reply_message(
            r"""Please provide a SSID cookie value to log into Kijiji\. To get this value:

1\. Log into Kijiji on any browser, with `Keep me signed in` checked
2\. Using a web inspector, copy the value of the `ssid` cookie in the domain `www\.kijiji\.ca`

Ensure that you do not log out of the Kijiji session afterwards\.
If you do, you will need another SSID cookie value to authenticate again\.""",
            parse_mode="MarkdownV2",
        )

        raise Exception("missing SSID cookie value")

    interface.reply_message("Logging into Kijiji...")

    try:
        ssid = args[0]

        KijijiBot(ssid)

        interface.reply_message("Successfully logged into Kijiji!")

        users_table = UsersTable(event["user_id"])
        users_table.user = {"ssid": ssid}
    except Exception:
        interface.reply_message("Failed to log into Kijiji.")
        raise
