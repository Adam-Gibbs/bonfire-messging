from endpoints.helpers.getRequestData import get_body, check_fields
from endpoints.user_methods.getUsername import get_username
from endpoints.helpers.returns import generate_response
from endpoints.exceptions import handle_exception
from endpoints.user_methods.checkFriends import check_friends
from endpoints.helpers.uniqueKey import unique_key
import boto3
import os


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
            return generate_response(200, {
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
