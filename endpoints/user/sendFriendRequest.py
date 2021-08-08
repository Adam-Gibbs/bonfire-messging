import os

import boto3
from endpoints.exceptions import handle_exception
from endpoints.helpers.getRequestData import check_fields, get_body
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.checkFriends import check_friends
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(["username", "message"], [str, str], event)
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    message = params['message']

    try:
        if username in check_friends(current_user):
            return generate_response(200, {
                "success": False,
                "message": "Already Friends"
            })

        client_db.put_item(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            Item={
                'friendRequestId': {'S': current_user+username},
                'requestFrom': {'S': current_user},
                'requestTo': {'S': username},
                'message': {'S': message}
            }
        )

        return generate_response(200, {
            "success": True,
            "message": "Request sent"
        })

    except Exception as e:
        return handle_exception(e)
