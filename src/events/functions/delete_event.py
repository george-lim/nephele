import shlex

from src.core.interface import Interface
from src.events.scheduler import Scheduler


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        args = shlex.split(event["command"])[1:]
    except Exception:
        interface.reply_message("Failed to parse input.")
        raise

    if len(args) < 1:
        interface.reply_message("Please provide an event name to delete.")
        raise Exception("missing event name")

    try:
        event_name = args[0]

        scheduler = Scheduler(event["user_id"])
        scheduler.delete_event(event_name)

        interface.reply_message("Successfully deleted event!")
    except Exception:
        interface.reply_message("Failed to delete event.")
        raise
