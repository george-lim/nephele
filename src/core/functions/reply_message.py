from src.core.interface import Interface


def handler(event, context=None):
    interface = Interface(event["interface"])
    interface.reply_message(event["message"], event.get("parseMode"))
