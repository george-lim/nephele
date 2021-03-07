from src.core.dynamodb.users_table import UsersTable
from src.core.interface import Interface


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        users_table = UsersTable(event["user_id"])
        users_table.user = {}

        interface.reply_message("Successfully logged out of TextNow!")
    except Exception:
        interface.reply_message("Failed to log out of TextNow.")
        raise
