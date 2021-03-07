from src.telegram.interface import TelegramInterface


def Interface(interface):
    if interface["name"] == TelegramInterface.get_name():
        return TelegramInterface(interface)

    raise Exception("invalid interface name")
