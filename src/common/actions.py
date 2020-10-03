import os
from src.common import telegram

_TELEGRAM_INTERFACE_NAME = os.environ.get('TELEGRAM_INTERFACE_NAME')

def reply_document(interface, document_path):
  if interface['name'] == _TELEGRAM_INTERFACE_NAME:
    return telegram.send_document(interface['chatId'], document_path)

  raise Exception('Unknown interface name')

def reply_message(interface, message, parse_mode=None):
  if interface['name'] == _TELEGRAM_INTERFACE_NAME:
    return telegram.send_message(interface['chatId'], message, parse_mode)

  raise Exception('Unknown interface name')
