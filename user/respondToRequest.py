from helpers.getRequestData import get_body, check_fields
from user_methods.getUsername import get_username
from chat_methods.createChat import create_chat
from helpers.returns import generate_response
from exceptions import handle_exception
import boto3
import os


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["friendRequestId", "accepted"],
        [str, bool],
        event
    )
    if invalid_fields is not None:
        return invalid_fields

    friend_request_id = params['friendRequestId']
    accepted = params['accepted']

    try:
        if accepted is True:
            response = client_db.get_item(
                TableName=os.environ['FRIEND_REQUESTS_TABLE'],
                Key={
                    'friendRequestId': {'S': friend_request_id}
                }
            )

            if 'Item' not in response:
                return generate_response(400, {
                    "success": False,
                    "message": "This friend request does not exist"
                })

            other_user = response.get('Item').get("requestFrom").get("S")

            client_db.put_item(
                TableName=os.environ['FRIENDS_TABLE'],
                Item={
                    'friendLinkId': {'S': current_user+other_user},
                    'friendTo': {'S': other_user},
                    'friendOf': {'S': current_user}
                }
            )

        client_db.delete_item(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            Key={
                'friendRequestId': {'S': friend_request_id}
            }
        )

        create_chat(current_user, None, other_user)

        return generate_response(200, {
            "success": True
        })

    except Exception as e:
        return handle_exception(e)
