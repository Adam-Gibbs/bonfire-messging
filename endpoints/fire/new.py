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
        ["message", "location", "public"],
        [str, str, bool],
        event,
        ["recipients"],
        [list]
    )
    if invalid_fields is not None:
        return invalid_fields

    message = params['message']
    location = params['location']
    public = params['public']
    recipients = []
    if "recipients" in params:
        recipients = params["recipients"]

    try:
        if not public and len(recipients) < 1:
            return generate_response(400, {
                    "success": False,
                    "message": "Your private chat does "
                               "not specify any recipients"
                })

        elif public and len(recipients) > 0:
            return generate_response(400, {
                    "success": False,
                    "message": "Your public chat can "
                               "not specify any recipients"
                })

        friends = check_friends(current_user)
        for recipient in recipients:
            if recipient not in friends:
                return generate_response(400, {
                    "success": False,
                    "message": f"You are not friends with {recipient}"
                })

        fire_id = str(unique_key(current_user))
        client_db.put_item(
            TableName=os.environ['FIRES_TABLE'],
            Item={
                'fireId': {'S': fire_id},
                'location': {'S': location},
                'publicFire': {'S': str(public)},
                'message': {'S': message}
            }
        )

        for recipient in recipients:
            client_db.put_item(
                TableName=os.environ['RECIPIENTS_TABLE'],
                Item={
                    'recipientId': {'S': (fire_id + recipient)},
                    'fireId': {'S': fire_id},
                    'username': {'S': recipient}
                }
            )

        return generate_response(200, {
            "success": True,
            "message": "Fire created"
        })

    except Exception as e:
        return handle_exception(e)
