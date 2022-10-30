from epicstore_api import EpicGamesStoreAPI
from nephele.command import Command
from nephele.events import Events
from nephele.telegram import Telegram

_EVENT_NAME = "epic-games-store-offers"
_EVENT_CRON_EXPRESSION = "0 22 ? * 5 *"


def _get_offer_urls():
    api = EpicGamesStoreAPI()
    games = api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]
    offer_urls = []

    for game in games:
        original_price = game["price"]["totalPrice"]["originalPrice"]
        discount_price = game["price"]["totalPrice"]["discountPrice"]

        if original_price == 0 or discount_price != 0:
            continue

        offer_urls.append(
            f"https://store.epicgames.com/p/{game['catalogNs']['mappings'][0]['pageSlug']}"
        )

    return offer_urls


def check_offers(event):
    telegram = Telegram(event)

    try:
        offer_urls = _get_offer_urls()
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while fetching offer URLs from Epic Games Store."
        )

        raise

    if len(offer_urls) == 0:
        telegram.send_message("There are no offers available on Epic Games Store.")
    else:
        telegram.send_message(f"Found {len(offer_urls)} offer(s) on Epic Games Store:")
        [telegram.send_message(offer_url) for offer_url in offer_urls]


def subscribe_offers(event):
    events = Events(event)
    telegram = Telegram(event)

    event["text"] = Command.SCHEDULE_EPIC_GAMES_STORE_CHECK_OFFERS.value
    event["is_scheduled"] = True

    try:
        events.put_rule(_EVENT_NAME, event, _EVENT_CRON_EXPRESSION)

        telegram.send_message(
            "Done! You will receive notifications for offers on Epic Games Store."
        )
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while creating Epic Games Store offers event."
        )

        raise


def unsubscribe_offers(event):
    events = Events(event)
    telegram = Telegram(event)

    try:
        events.delete_rule(_EVENT_NAME)

        telegram.send_message(
            "Done! You will stop receiving notifications for offers on Epic Games Store."
        )
    except events.ResourceNotFoundException:
        telegram.send_message(
            "You are not currently receiving notifications for offers on Epic Games Store."
        )
    except Exception:
        telegram.send_message(
            "An unexpected error occurred while deleting Epic Games Store offers event."
        )

        raise
