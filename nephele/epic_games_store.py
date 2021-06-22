from epicstore_api import EpicGamesStoreAPI
from nephele.command import Command
from nephele.events import Events
from nephele.telegram import Telegram

_EVENT_NAME = "epic-games-store-offers"
_EVENT_CRON_EXPRESSION = "0 22 ? * 5 *"


def _get_offer_urls():
    api = EpicGamesStoreAPI()
    free_games = api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]
    offer_urls = []

    for free_game in free_games:
        promotions = free_game.get("promotions")

        if promotions and promotions.get("promotionalOffers"):
            product_slug = free_game["productSlug"].split("/", 1)[0]
            product = api.get_product(product_slug)

            offers = []
            addon_offers = []

            for page in product["pages"]:
                if page["type"] == "productHome":
                    offers.append(page["offer"])
                elif page["type"] in ["addon", "offer"]:
                    addon_offers.append(page["offer"])

            offers.extend(addon_offers)

            offer_urls.extend(
                map(
                    lambda x: f"https://www.epicgames.com/store/purchase?namespace={x['namespace']}&offers={x['id']}",
                    offers,
                )
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
