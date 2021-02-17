from lib.telegram.interface import TelegramInterface

_interfaces = { TelegramInterface.get_name(): TelegramInterface }

def Interface(interface):
  interface_name = interface['name']
  return _interfaces[interface_name](interface)
