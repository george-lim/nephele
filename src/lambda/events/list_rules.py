import json
import os
import shlex
from src.common.actions import reply_message
from src.common.events import list_rules, list_targets_by_rule

_RESOURCE_PREFIX = os.environ.get('RESOURCE_PREFIX')

def handler(event, context):
  interface = event['interface']
  user_id = interface['userId']
  formatted_rules = []

  try:
    rule_name_prefix = f'{_RESOURCE_PREFIX}-{user_id}_'
    rules = list_rules(rule_name_prefix)

    for rule in rules:
      targets = list_targets_by_rule(rule['Name'])

      formatted_rules.append({
        'rule_name': rule['Name'][len(rule_name_prefix):],
        'state': rule['State'],
        'cron_expression': rule['ScheduleExpression'][len('cron('):-len(')')],
        'command': json.loads(targets[0]['Input'])['command']
      })
  except:
    reply_message(interface, 'Failed to list rules.')
    raise

  if not formatted_rules:
    reply_message(interface, 'No rules found!')
    return

  for rule in formatted_rules:
    reply_message(interface, f'''Name: {rule['rule_name']}
State: {rule['state']}
Cron Expression: {rule['cron_expression']}
Command: {rule['command']}''')
