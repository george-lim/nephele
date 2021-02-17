import boto3
import json
import os

_RESOURCE_PREFIX = os.environ.get('RESOURCE_PREFIX')
_TARGET_ROLE_ARN = os.environ.get('TARGET_ROLE_ARN')

_events = boto3.client('events')

class Scheduler:
  def __init__(self, user_id):
    self.namespace = f'{_RESOURCE_PREFIX}-{user_id}'

  def _get_rule_name(self, event_name):
    return f'{self.namespace}_{event_name}'

  def _get_target_id(self, rule_name):
    return f'{rule_name}_target'

  def delete_event(self, event_name):
    rule_name = self._get_rule_name(event_name)
    target_ids = [self._get_target_id(rule_name)]

    _events.remove_targets(Rule=rule_name, Ids=target_ids)
    _events.delete_rule(Name=rule_name)

  def disable_event(self, event_name):
    _events.disable_rule(Name=self._get_rule_name(event_name))

  def enable_event(self, event_name):
    _events.enable_rule(Name=self._get_rule_name(event_name))

  def list_events(self):
    events = []
    next_token = ''

    while next_token is not None:
      kwargs = { 'NamePrefix': self.namespace }

      if next_token:
        kwargs['NextToken'] = next_token

      response = _events.list_rules(**kwargs)
      next_token = response.get('NextToken')

      for rule in response['Rules']:
        response = _events.list_targets_by_rule(Rule=rule['Name'])
        target = response['Targets'][0]

        events.append({
          'name': rule['Name'][len(self.namespace)+1:],
          'state': rule['State'],
          'cron_expression': rule['ScheduleExpression'][len('cron('):-len(')')],
          'command': json.loads(target['Input'])['command']
        })

    return events

  def put_event(self, event_name, cron_expression, target_arn, event):
    rule_name = self._get_rule_name(event_name)
    schedule_expression = f'cron({cron_expression})'

    targets = [{
      'Id': self._get_target_id(rule_name),
      'Arn': target_arn,
      'RoleArn': _TARGET_ROLE_ARN,
      'Input': json.dumps(event)
    }]

    _events.put_rule(Name=rule_name, ScheduleExpression=schedule_expression)
    _events.put_targets(Rule=rule_name, Targets=targets)
