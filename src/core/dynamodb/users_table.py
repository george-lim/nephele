import os

import boto3


class UsersTable:
    def __init__(self, user_id):
        dynamodb = boto3.resource("dynamodb")
        table_name = os.environ["USERS_TABLE_NAME"]
        self.table = dynamodb.Table(table_name)

        self.key = {"userId": user_id}
        self.service_name = os.environ["SERVICE_NAME"]

    @property
    def user(self):
        response = self.table.get_item(
            Key=self.key, ProjectionExpression=self.service_name
        )

        return response.get("Item", {}).get(self.service_name, {})

    @user.setter
    def user(self, user):
        update_expression = f"SET {self.service_name} = :val"
        expression_attribute_values = {":val": user}

        self.table.update_item(
            Key=self.key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
