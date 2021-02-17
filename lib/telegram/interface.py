import os
import requests

_TELEGRAM_INTERFACE_NAME = os.environ.get('TELEGRAM_INTERFACE_NAME')
_TELEGRAM_REQUEST_ARN = os.environ.get('TELEGRAM_REQUEST_ARN')
_TELEGRAM_REQUEST_BASE_URL = os.environ.get('TELEGRAM_REQUEST_BASE_URL')

class TelegramInterface:
  def __init__(self, interface):
    self.chat_id = interface['chatId']

  @staticmethod
  def get_name():
    return _TELEGRAM_INTERFACE_NAME

  @staticmethod
  def get_request_arn():
    return _TELEGRAM_REQUEST_ARN

  def reply_document(self, document_path):
    url = f'{_TELEGRAM_REQUEST_BASE_URL}/sendDocument'
    data = { 'chat_id': self.chat_id }
    files = { 'document': (document_path.name, document_path.read_bytes()) }

    response = requests.post(url, data, files=files)
    response.raise_for_status()

  def reply_message(self, text, parse_mode=None):
    url = f'{_TELEGRAM_REQUEST_BASE_URL}/sendMessage'
    data = { 'chat_id': self.chat_id, 'text': text }

    if parse_mode:
      data['parse_mode'] = parse_mode

    response = requests.post(url, data)
    response.raise_for_status()

  def reply_photo(self, photo_path):
    url = f'{_TELEGRAM_REQUEST_BASE_URL}/sendPhoto'
    data = { 'chat_id': self.chat_id }
    files = { 'photo': (photo_path.name, photo_path.read_bytes()) }

    response = requests.post(url, data, files=files)
    response.raise_for_status()
