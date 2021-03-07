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
        interface.reply_message(
            "Please provide an event name, cron expression, and command to put."
        )

        raise Exception("missing event details")

    try:
        [event_name, cron_expression, *command_args] = [*args]
        event["command"] = " ".join(command_args)

        scheduler = Scheduler(event["user_id"])

        scheduler.put_event(
            event_name, cron_expression, interface.get_request_arn(), event
        )

        interface.reply_message("Successfully put event!")
    except Exception:
        interface.reply_message("Failed to put event.")

        raise
