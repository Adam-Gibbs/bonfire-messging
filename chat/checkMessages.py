import os

import boto3
from auth.authExceptions import handle_auth_exception
from helpers.getRequestData import check_fields, get_body
from helpers.returns import generate_response
from user_methods.getUsername import get_username
from user_methods.userChats import get_all_chat_ids


def lambda_handler(event, context):
    try:
        params = get_body(event)
        current_user = get_username(event)
        client_db = boto3.client('dynamodb')

        invalid_fields = check_fields(
            ["chat"],
            [int],
            event,
            ["time"],
            [int]
        )
        if invalid_fields is not None:
            return invalid_fields

        chat_id = str(params['chat'])
        time = 0
        if "time" in params:
            time = params["time"]

        if chat_id not in get_all_chat_ids(current_user):
            return generate_response(400, {
                "success": False,
                "message": "You are not in that chat"
            })

        resp = client_db.query(
            TableName=os.environ['MESSAGES_TABLE'],
            IndexName='chatId-sent-index',
            KeyConditionExpression='chatId = :chat_id AND sent > :sent',
            ExpressionAttributeValues={
                ':chat_id': {'S': chat_id},
                ':sent': {'S': str(time)}
            }
        )

        resp_items = []
        if 'Items' in resp:
            resp_items = resp.get("Items")

        return generate_response(200, {
            "messages": resp_items,
        })

    except Exception as e:
        return handle_auth_exception(e)
