import shlex
from io import BytesIO
from pathlib import Path
from time import strftime
from zipfile import ZipFile

import requests
from kijiji_bot import KijijiBot
from nephele.command import Command
from nephele.events import Events
from nephele.telegram import Telegram

_EVENT_NAME = "kijiji-repost"


def repost_ads(event):
    telegram = Telegram(event)

    cookie = event["kijiji_cookie"]
    ads_url = event["kijiji_ads_url"]
    ads_path = Path(f"/tmp/{event['namespace']}/ads")
    is_using_alternate_ads = int(strftime("%j")) % 2 == 0
    post_delay_seconds = 0

    try:
        response = requests.get(ads_url)
        response.raise_for_status()
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while downloading Kijiji ads."
        )

        raise

    try:
        with ZipFile(BytesIO(response.content)) as archive:
            archive.extractall(ads_path)
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while extracting Kijiji ads."
        )

        raise

    try:
        bot = KijijiBot(cookie)
    except Exception:
        telegram.send_message("An unexpected error occurred while logging into Kijiji.")
        raise

    try:
        bot.repost_ads(ads_path, is_using_alternate_ads, post_delay_seconds)
    except Exception as exception:
        print(exception)

        # Do not raise exception because it's possible some ads failed to repost while others succeeded.


def check_repost_event_status(event):
    events = Events(event)
    telegram = Telegram(event)

    try:
        rule_info = events.describe_rule(_EVENT_NAME)

        telegram.send_message(
            f"""Cookie (ssid): {rule_info["event"]["kijiji_cookie"]}
Ads URL: {rule_info["event"]["kijiji_ads_url"]}
Cron Expression: {rule_info["cron_expression"]}"""
        )
    except events.ResourceNotFoundException:
        telegram.send_message(
            f"You don't have a Kijiji repost event setup yet. Use {Command.SET_KIJIJI_REPOST_EVENT.value} to create an event first."  # noqa: E501
        )
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while checking Kijiji repost event status."
        )

        raise


def set_repost_event(event):
    events = Events(event)
    telegram = Telegram(event)

    args = shlex.split(event["text"])[1:]

    if len(args) < 3:
        telegram.send_message(
            f"usage: {Command.SET_KIJIJI_REPOST_EVENT.value} <ssid cookie> <ads url> <cron expression>"
        )

        return

    event["text"] = Command.SCHEDULE_KIJIJI_REPOST_ADS.value
    event["is_scheduled"] = True
    event["kijiji_cookie"] = args[0]
    event["kijiji_ads_url"] = args[1]
    cron_expression = args[2]

    telegram.send_message("Testing Kijiji repost event...")
    repost_ads(event)

    try:
        events.put_rule(_EVENT_NAME, event, cron_expression)
        telegram.send_message("Done! Your Kijiji ads will be reposted periodically.")
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while creating Kijiji repost event."
        )

        raise


def delete_repost_event(event):
    events = Events(event)
    telegram = Telegram(event)

    try:
        events.delete_rule(_EVENT_NAME)
        telegram.send_message("Done! You have deleted the Kijiji repost event.")
    except events.ResourceNotFoundException:
        telegram.send_message("You don't have a Kijiji repost event setup yet.")
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while deleting Kijiji repost event."
        )

        raise
