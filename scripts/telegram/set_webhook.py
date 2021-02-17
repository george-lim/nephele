import appdirs
import json
import pathlib
import requests
import sys

log = lambda msg: print(f'Serverless: \x1b[0;33m{msg}\x1b[0m')

[org, app, stage, serverless_outputs_str_path] = [*sys.argv[1:]]
user_cache_path = pathlib.Path(appdirs.user_cache_dir(app, org))
serverless_outputs_path = pathlib.Path(serverless_outputs_str_path)

config_path = user_cache_path.joinpath('telegram_config.json')
outputs = json.loads(serverless_outputs_path.read_text())

webhook_url = f'{outputs["ServiceEndpoint"]}/{outputs["TelegramWebhookPath"]}'
config = json.loads(config_path.read_text()) if config_path.exists() else { 'has_set_webhook': {} }

if config['has_set_webhook'].get(stage):
  log('Telegram webhook is already set.')
  log(f'Skip setting Telegram webhook: {webhook_url}')
elif not outputs['TelegramBotApiToken']:
  log('Missing Telegram Bot API token.')
  log(f'Skip setting Telegram webhook: {webhook_url}')
else:
  log(f'Setting Telegram webhook: {webhook_url}')

  url = outputs['TelegramSetWebhookUrl']
  data = { 'url': webhook_url }

  response = requests.post(url, data)
  response.raise_for_status()

  if not config_path.parent.exists():
    config_path.parent.mkdir(0o755, True)

  config['has_set_webhook'][stage] = True
  config_path.write_text(json.dumps(config))
