from enum import Enum


class Command(Enum):
    # Schedule commands
    SCHEDULE_EPIC_GAMES_STORE_CHECK_OFFERS = "/scheduleepicgamesstorecheckoffers"
    SCHEDULE_KIJIJI_REPOST_ADS = "/schedulekijijirepostads"
    SCHEDULE_TEXTNOW_SEND_SMS = "/scheduletextnowsendsms"

    # User commands
    START = "/start"
    HELP = "/help"
    SUBSCRIBE_EPIC_GAMES_STORE_OFFERS = "/subscribeepicgamesstoreoffers"
    UNSUBSCRIBE_EPIC_GAMES_STORE_OFFERS = "/unsubscribeepicgamesstoreoffers"
    MY_KIJIJI_REPOST_EVENT = "/mykijijirepostevent"
    SET_KIJIJI_REPOST_EVENT = "/setkijijirepostevent"
    DELETE_KIJIJI_REPOST_EVENT = "/deletekijijirepostevent"
    MY_TEXTNOW_MESSAGE_EVENT = "/mytextnowmessageevent"
    SET_TEXTNOW_MESSAGE_EVENT = "/settextnowmessageevent"
    DELETE_TEXTNOW_MESSAGE_EVENT = "/deletetextnowmessageevent"

    @property
    def description(self):
        if self is Command.SUBSCRIBE_EPIC_GAMES_STORE_OFFERS:
            return (
                f"{self.value} - receive notifications for offers on Epic Games Store"
            )
        elif self is Command.UNSUBSCRIBE_EPIC_GAMES_STORE_OFFERS:
            return f"{self.value} - stop receiving notifications for offers on Epic Games Store"
        elif self is Command.MY_KIJIJI_REPOST_EVENT:
            return f"{self.value} - get status of Kijiji repost event"
        elif self is Command.SET_KIJIJI_REPOST_EVENT:
            return f"{self.value} - schedule an event to periodically repost Kijiji ads"
        elif self is Command.DELETE_KIJIJI_REPOST_EVENT:
            return f"{self.value} - delete Kijiji repost event"
        elif self is Command.MY_TEXTNOW_MESSAGE_EVENT:
            return f"{self.value} - get status of TextNow message event"
        elif self is Command.SET_TEXTNOW_MESSAGE_EVENT:
            return (
                f"{self.value} - schedule an event to periodically send a SMS message"
            )
        elif self is Command.DELETE_TEXTNOW_MESSAGE_EVENT:
            return f"{self.value} - delete TextNow message event"
        else:
            return self.value
