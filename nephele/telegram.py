import os

import requests
from nephele.command import Command


class Telegram:
    def __init__(self, event):
        self._session = requests.Session()
        self._bot_api_url = os.environ["telegramBotApiUrl"]
        self._chat_id = event["chatId"]

        self._markdown_v2_escape_set = {
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        }

    def escape_markdown_v2(self, string):
        return "".join(
            [f"\\{ch}" if ch in self._markdown_v2_escape_set else ch for ch in string]
        )

    def send_message(self, text, parse_mode=None):
        url = f"{self._bot_api_url}/sendMessage"
        data = {"chat_id": self._chat_id, "text": text}

        if parse_mode is not None:
            data["parse_mode"] = parse_mode

        response = self._session.post(url, data)
        response.raise_for_status()
        return response


def send_invalid_command_message(event):
    telegram = Telegram(event)
    telegram.send_message("Please send a valid command.")


def send_help_message(event):
    telegram = Telegram(event)

    text = telegram.escape_markdown_v2(
        f"""I can help you access George's cloud-compatible side projects.

You can control me by sending these commands:

*Epic Games Store*
{Command.SUBSCRIBE_EPIC_GAMES_STORE_OFFERS.description}
{Command.UNSUBSCRIBE_EPIC_GAMES_STORE_OFFERS.description}

*Kijiji*
{Command.MY_KIJIJI_REPOST_EVENT.description}
{Command.SET_KIJIJI_REPOST_EVENT.description}
{Command.DELETE_KIJIJI_REPOST_EVENT.description}

*TextNow*
{Command.MY_TEXTNOW_MESSAGE_EVENT.description}
{Command.SET_TEXTNOW_MESSAGE_EVENT.description}
{Command.DELETE_TEXTNOW_MESSAGE_EVENT.description}"""
    )

    text = text.replace("\\*Epic Games Store\\*", "*Epic Games Store*")
    text = text.replace("\\*Kijiji\\*", "*Kijiji*")
    text = text.replace("\\*TextNow\\*", "*TextNow*")

    telegram.send_message(text, "MarkdownV2")
