import shlex
from pathlib import Path

import pytextnow
from nephele.command import Command
from nephele.events import Events
from nephele.telegram import Telegram

_EVENT_NAME = "textnow-message"


def send_sms(event):
    telegram = Telegram(event)

    username = event["textnow_username"]
    sid_cookie = event["textnow_sid_cookie"]
    csrf_cookie = event["textnow_csrf_cookie"]
    to = event["textnow_to"]
    text = event["textnow_text"]
    user_cookies_file = Path(f"/tmp/{event['namespace']}/user_cookies.json")

    try:
        client = pytextnow.Client(username, sid_cookie, csrf_cookie, user_cookies_file)
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while logging into TextNow."
        )

        raise

    try:
        client.send_sms(to, text)
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while sending SMS from TextNow."
        )

        raise


def check_message_event_status(event):
    events = Events(event)
    telegram = Telegram(event)

    try:
        rule_info = events.describe_rule(_EVENT_NAME)

        telegram.send_message(
            f"""Username: {rule_info["event"]["textnow_username"]}
Cookie (connect.sid): {rule_info["event"]["textnow_sid_cookie"]}
Cookie (_csrf): {rule_info["event"]["textnow_csrf_cookie"]}
To: {rule_info["event"]["textnow_to"]}
Text: {rule_info["event"]["textnow_text"]}
Cron Expression: {rule_info["cron_expression"]}"""
        )
    except events.ResourceNotFoundException:
        telegram.send_message(
            f"You don't have a TextNow message event setup yet. Use {Command.SET_TEXTNOW_MESSAGE_EVENT.value} to create an event first."  # noqa: E501
        )
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while checking TextNow message event status."
        )

        raise


def set_message_event(event):
    events = Events(event)
    telegram = Telegram(event)

    args = shlex.split(event["text"])[1:]

    if len(args) < 5:
        telegram.send_message(
            f"usage: {Command.SET_TEXTNOW_MESSAGE_EVENT.value} <username> <connect.sid cookie> <_csrf cookie> <recipient> <text> <cron expression>"  # noqa: E501
        )

        return

    event["text"] = Command.SCHEDULE_TEXTNOW_SEND_SMS.value
    event["is_scheduled"] = True
    event["textnow_username"] = args[0]
    event["textnow_sid_cookie"] = args[1]
    event["textnow_csrf_cookie"] = args[2]
    event["textnow_to"] = args[3]
    event["textnow_text"] = args[4]
    cron_expression = args[5]

    telegram.send_message("Testing TextNow message event...")
    send_sms(event)

    try:
        events.put_rule(_EVENT_NAME, event, cron_expression)

        telegram.send_message(
            "Done! The SMS message will be sent periodically to your recipient."
        )
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while creating TextNow message event."
        )

        raise


def delete_message_event(event):
    events = Events(event)
    telegram = Telegram(event)

    try:
        events.delete_rule(_EVENT_NAME)
        telegram.send_message("Done! You have deleted the TextNow message event.")
    except events.ResourceNotFoundException:
        telegram.send_message("You don't have a TextNow message event setup yet.")
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while deleting TextNow message event."
        )

        raise
