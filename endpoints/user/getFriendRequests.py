import os

import boto3
from boto3.dynamodb.conditions import Key
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    try:
        resp = client_db.get_item(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            IndexName='to-index',
            KeyConditionExpression=Key('to').eq(current_user)
        )

        print(resp)

        generate_response(200,  {
            "resp": resp
        })

    except Exception as e:
        return handle_exception(e)
