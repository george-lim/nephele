import json
import sys
from pathlib import Path

import requests


def log(message):
    print(f"Serverless: \x1b[0;33m{message}\x1b[0m")


serverless_outputs_path_str = sys.argv[1]
serverless_outputs_path = Path(serverless_outputs_path_str)
outputs = json.loads(serverless_outputs_path.read_text())

webhook_url = f"{outputs['ServiceEndpoint']}/{outputs['TelegramWebhookPath']}"

if len(outputs["TelegramBotApiToken"]) == 0:
    log("Missing Telegram Bot API token.")
    log("Failed to set Telegram webhook.")
else:
    url = outputs["TelegramSetWebhookUrl"]
    data = {"url": webhook_url}

    response = requests.post(url, data)
    response.raise_for_status()

    log(f"Successfully set Telegram webhook: {webhook_url}")
