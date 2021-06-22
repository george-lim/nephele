import shlex

from nephele import epic_games_store, kijiji, telegram, textnow
from nephele.command import Command


def handler(event, context=None):
    try:
        command = shlex.split(event["text"])[0]
    except Exception:
        telegram.send_invalid_command_message(event)
        raise

    if event.get("is_scheduled"):
        if command == Command.SCHEDULE_EPIC_GAMES_STORE_CHECK_OFFERS.value:
            epic_games_store.check_offers(event)
        elif command == Command.SCHEDULE_KIJIJI_REPOST_ADS.value:
            kijiji.repost_ads(event)
        elif command == Command.SCHEDULE_TEXTNOW_SEND_SMS.value:
            textnow.send_sms(event)
    elif command == Command.START.value:
        telegram.send_help_message(event)
    elif command == Command.HELP.value:
        telegram.send_help_message(event)
    elif command == Command.SUBSCRIBE_EPIC_GAMES_STORE_OFFERS.value:
        epic_games_store.subscribe_offers(event)
    elif command == Command.UNSUBSCRIBE_EPIC_GAMES_STORE_OFFERS.value:
        epic_games_store.unsubscribe_offers(event)
    elif command == Command.MY_KIJIJI_REPOST_EVENT.value:
        kijiji.check_repost_event_status(event)
    elif command == Command.SET_KIJIJI_REPOST_EVENT.value:
        kijiji.set_repost_event(event)
    elif command == Command.DELETE_KIJIJI_REPOST_EVENT.value:
        kijiji.delete_repost_event(event)
    elif command == Command.MY_TEXTNOW_MESSAGE_EVENT.value:
        textnow.check_message_event_status(event)
    elif command == Command.SET_TEXTNOW_MESSAGE_EVENT.value:
        textnow.set_message_event(event)
    elif command == Command.DELETE_TEXTNOW_MESSAGE_EVENT.value:
        textnow.delete_message_event(event)
    else:
        telegram.send_help_message(event)
