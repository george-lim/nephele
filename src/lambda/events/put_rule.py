import json
import os
import shlex
from src.common.actions import reply_message
from src.common.events import put_rule, put_target

_RESOURCE_PREFIX = os.environ.get('RESOURCE_PREFIX')
_TARGET_ROLE_ARN = os.environ.get('TARGET_ROLE_ARN')
_TELEGRAM_INTERFACE_NAME = os.environ.get('TELEGRAM_INTERFACE_NAME')
_TELEGRAM_REQUEST_ARN = os.environ.get('TELEGRAM_REQUEST_ARN')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']
  args = None
  target_arn = None

  try:
    args = shlex.split(event['command'])[1:]
  except:
    reply_message(interface, 'Failed to parse input.')
    raise

  if interface['name'] == _TELEGRAM_INTERFACE_NAME:
    target_arn = _TELEGRAM_REQUEST_ARN
  else:
    raise Exception('Unknown interface name')

  if len(args) < 3:
    reply_message(interface, 'Please provide an event name, cron expression, and command.')
    raise Exception('Missing event rule info')

  try:
    [rule_name, cron_expression, *command_args] = [*args]

    rule_name = f'{_RESOURCE_PREFIX}-{user_id}_{rule_name}'
    put_rule(rule_name, f'cron({cron_expression})')

    command = ' '.join(command_args)
    target_input = json.dumps({ 'command': command, 'interface': interface })
    put_target(rule_name, f'{rule_name}_target', target_arn, _TARGET_ROLE_ARN, target_input)
  except:
    reply_message(interface, 'Failed to put rule - input may be invalid.')
    raise

  reply_message(interface, 'Successfully put rule!')
