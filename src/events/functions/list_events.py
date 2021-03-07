from src.core.interface import Interface
from src.events.scheduler import Scheduler


def handler(event, context=None):
    interface = Interface(event["interface"])

    try:
        scheduler = Scheduler(event["user_id"])
        events = scheduler.list_events()

        if len(events) == 0:
            interface.reply_message("No events found!")
        else:
            for event in events:
                interface.reply_message(
                    f"""Name: {event['name']}
State: {event['state']}
Cron Expression: {event['cron_expression']}
Command: {event['command']}"""
                )
    except Exception:
        interface.reply_message("Failed to list events.")
        raise
