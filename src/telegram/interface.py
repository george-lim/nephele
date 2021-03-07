import os

import requests


class TelegramInterface:
    def __init__(self, interface):
        self.request_base_url = os.environ["TELEGRAM_REQUEST_BASE_URL"]
        self.chat_id = interface["chat_id"]
        self.session = requests.Session()

    @staticmethod
    def get_name():
        return os.environ["TELEGRAM_INTERFACE_NAME"]

    @staticmethod
    def get_request_arn():
        return os.environ["TELEGRAM_REQUEST_ARN"]

    def reply_document(self, document_path):
        url = f"{self.request_base_url}/sendDocument"
        data = {"chat_id": self.chat_id}
        files = {"document": (document_path.name, document_path.read_bytes())}

        response = self.session.post(url, data, files=files)
        response.raise_for_status()

        return response

    def reply_message(self, message, parse_mode=None):
        url = f"{self.request_base_url}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}

        if parse_mode is not None:
            data["parse_mode"] = parse_mode

        response = self.session.post(url, data)
        response.raise_for_status()

        return response

    def reply_photo(self, photo_path):
        url = f"{self.request_base_url}/sendPhoto"
        data = {"chat_id": self.chat_id}
        files = {"photo": (photo_path.name, photo_path.read_bytes())}

        response = self.session.post(url, data, files=files)
        response.raise_for_status()

        return response
