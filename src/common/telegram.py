import os
import requests

_TELEGRAM_REQUEST_BASE_URL = os.environ.get('TELEGRAM_REQUEST_BASE_URL')

def send_document(chat_id, document_path):
  with open(document_path, 'rb') as file:
    return requests.post(
      f'{_TELEGRAM_REQUEST_BASE_URL}/sendDocument',
      data={ 'chat_id': chat_id },
      files={ 'document': (document_path.name, file) }
    )

def send_message(chat_id, text, parse_mode=None):
  data = {
    'chat_id': chat_id,
    'text': text
  }

  if parse_mode:
    data['parse_mode'] = parse_mode

  return requests.post(f'{_TELEGRAM_REQUEST_BASE_URL}/sendMessage', data=data)
