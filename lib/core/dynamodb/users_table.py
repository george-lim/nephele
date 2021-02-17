import boto3
import json
import os

_SERVICE_NAME = os.environ.get('SERVICE_NAME')
_USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME')

_dynamodb = boto3.resource('dynamodb')

class UsersTable:
  def __init__(self, user_id):
    self.table = _dynamodb.Table(_USERS_TABLE_NAME)
    self.key = { 'userId': user_id }

  def get_user(self):
    response = self.table.get_item(Key=self.key, ProjectionExpression=_SERVICE_NAME)

    user_str = response.get('Item', {}).get(_SERVICE_NAME, '{}')
    return json.loads(user_str)

  def update_user(self, user):
    update_expression = f'SET {_SERVICE_NAME} = :val'
    expression_attribute_values = { ':val': json.dumps(user) }

    self.table.update_item(
      Key=self.key,
      UpdateExpression=update_expression,
      ExpressionAttributeValues=expression_attribute_values
    )
