import kijiji_bot
import os
import shlex
from src.common.actions import reply_message

_KIJIJI_SERVICE_NAME = os.environ.get('KIJIJI_SERVICE_NAME')

def handler(event, context):
  interface = event['interface']
  service_log_in = None
  user = {}
  args = None

  try:
    args = shlex.split(event['command'])[1:]
  except:
    reply_message(interface, 'Failed to parse input.')
    raise

  if event['serviceName'] == _KIJIJI_SERVICE_NAME:
    service_log_in = kijiji_bot.KijijiBot().login
  else:
    raise Exception('Unknown service name')

  if len(args) < 2:
    reply_message(interface, 'Please provide a username, password, and 2FA code (if required).')
    raise Exception('Missing account info')

  reply_message(interface, 'Logging in...')

  try:
    user['cookies'] = service_log_in(*args)
  except:
    reply_message(interface, 'Failed to log in - input may be invalid.')
    raise

  reply_message(interface, 'Successfully logged in!')
  return user
