import os
import time

import boto3
from exceptions import handle_exception
from helpers.getRequestData import check_fields, get_body
from helpers.returns import generate_response
from helpers.uniqueKey import unique_key
from user_methods.getUsername import get_username
from user_methods.userChats import get_all_chat_ids, chat_has_user


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["chat", "recipient", "message"],
        [int, str, str],
        event,
        ["replyId"],
        [int]
    )
    if invalid_fields is not None:
        return invalid_fields

    chat_id = str(params['chat'])
    recipient = params['recipient']
    message = params['message']
    reply_id = ""
    if "replyId" in params:
        reply_id = params["replyId"]

    try:
        if chat_id not in get_all_chat_ids(current_user):
            return generate_response(400, {
                "success": False,
                "message": "You are not in that chat"
            })

        if not chat_has_user(chat_id, recipient):
            return generate_response(400, {
                "success": False,
                "message": f"{recipient} is not a member of that chat"
            })

        unique = unique_key(
            current_user,
            os.environ['MESSAGES_TABLE'],
            'messageId'
        )
        client_db.put_item(
            TableName=os.environ['MESSAGES_TABLE'],
            Item={
                'messageId': {'S': str(unique)},
                'chatId': {'S': chat_id},
                'recipient': {'S': recipient},
                'replyId': {'S': str(reply_id)},
                'message': {'S': message},
                'time': {'S': str(time.time())}
            }
        )

        return generate_response(200, {
            "success": True,
            "message": "Message sent"
        })

    except Exception as e:
        return handle_exception(e)
