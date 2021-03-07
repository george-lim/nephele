from epic_games_bot import EpicGamesBot
from src.core.interface import Interface


def handler(event, context=None):
    interface = Interface(event["interface"])

    offer_urls = EpicGamesBot.list_free_promotional_offers()

    if len(offer_urls) == 0:
        interface.reply_message("No free promotional offers on Epic Games!")
    else:
        [interface.reply_message(offer_url) for offer_url in offer_urls]
