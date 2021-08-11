import os

import boto3
from endpoints.exceptions import handle_exception
from endpoints.helpers.getRequestData import check_fields, get_body
from endpoints.helpers.returns import generate_response
from endpoints.helpers.uniqueKey import unique_key
from endpoints.user_methods.checkFriends import check_friends
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["recipient", "message"],
        [str, str],
        event,
        ["replyId"],
        [int]
    )
    if invalid_fields is not None:
        return invalid_fields

    recipient = params['recipient']
    message = params['message']
    reply_id = ""
    if "replyId" in params:
        reply_id = params["replyId"]

    try:
        if recipient not in check_friends(current_user):
            return generate_response(400, {
                "success": False,
                "message": f"You are not friends with {recipient}"
            })

        client_db.put_item(
            TableName=os.environ['MESSAGES_TABLE'],
            Item={
                'messageId': {'S': str(unique_key(current_user))},
                'recipient': {'S': recipient},
                'replyId': {'S': str(reply_id)},
                'message': {'S': message}
            }
        )

        return generate_response(200, {
            "success": True,
            "message": "Message sent"
        })

    except Exception as e:
        return handle_exception(e)
