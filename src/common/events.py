import boto3

_events = boto3.client('events')

def delete_rule(rule_name):
  return _events.delete_rule(Name=rule_name)

def disable_rule(rule_name):
  return _events.disable_rule(Name=rule_name)

def enable_rule(rule_name):
  return _events.enable_rule(Name=rule_name)

def list_rules(rule_name_prefix):
  rules = []
  next_token = ''

  while next_token is not None:
    kwargs = { 'NamePrefix': rule_name_prefix }

    if next_token:
      kwargs['NextToken'] = next_token

    response = _events.list_rules(**kwargs)
    rules.extend(response['Rules'])
    next_token = response.get('NextToken')

  return rules

def list_targets_by_rule(rule_name):
  targets = []
  next_token = ''

  while next_token is not None:
    kwargs = { 'Rule': rule_name }

    if next_token:
      kwargs['NextToken'] = next_token

    response = _events.list_targets_by_rule(**kwargs)
    targets.extend(response['Targets'])
    next_token = response.get('NextToken')

  return targets

def put_rule(rule_name, schedule_expression):
  return _events.put_rule(Name=rule_name, ScheduleExpression=schedule_expression)

def put_target(rule_name, target_id, target_arn, target_role_arn, target_input):
  return _events.put_targets(
    Rule=rule_name,
    Targets=[{
      'Id': target_id,
      'Arn': target_arn,
      'RoleArn': target_role_arn,
      'Input': target_input
    }]
  )

def remove_target(rule_name, target_id):
  return _events.remove_targets(Rule=rule_name, Ids=[target_id])
