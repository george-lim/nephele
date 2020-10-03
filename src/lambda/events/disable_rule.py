import os
import shlex
from src.common.actions import reply_message
from src.common.events import disable_rule

_RESOURCE_PREFIX = os.environ.get('RESOURCE_PREFIX')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']
  args = None

  try:
    args = shlex.split(event['command'])[1:]
  except:
    reply_message(interface, 'Failed to parse input.')
    raise

  if len(args) < 1:
    reply_message(interface, 'Please provide an event name.')
    raise Exception('Missing event rule info')

  try:
    rule_name = f'{_RESOURCE_PREFIX}-{user_id}_{args[0]}'
    disable_rule(rule_name)
  except:
    reply_message(interface, 'Failed to disable rule - input may be invalid.')
    raise

  reply_message(interface, 'Successfully disabled rule!')
