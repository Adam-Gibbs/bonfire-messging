import os

import boto3
from auth.authExceptions import handle_auth_exception
from helpers.returns import generate_response
from user_methods.getUsername import get_username


def lambda_handler(event, context):
    try:
        current_user = get_username(event)
        client_db = boto3.client('dynamodb')

        resp = client_db.query(
            TableName=os.environ['MESSAGES_TABLE'],
            IndexName='recipient-index',
            KeyConditionExpression='recipient = :currentUser',
            ExpressionAttributeValues={
                ':currentUser': {'S': current_user}
            }
        )

        if 'Items' in resp:
            resp_items = resp.get("Items")
        else:
            resp_items = []

        return generate_response(200, {
            "messages": resp_items,
        })

    except Exception as e:
        return handle_auth_exception(e)
