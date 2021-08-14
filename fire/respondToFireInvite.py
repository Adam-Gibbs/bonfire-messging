from helpers.getRequestData import get_body, check_fields
from user_methods.getUsername import get_username
from chat_methods.createChat import add_chat_user
from helpers.returns import generate_response
from exceptions import handle_exception
import boto3
import os


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["recipientId", "accepted"],
        [str, bool],
        event
    )
    if invalid_fields is not None:
        return invalid_fields

    recipient_id = params['recipientId']
    accepted = params['accepted']

    try:
        if accepted is True:
            # Get fire id from recipients, check if invite exists
            resp = client_db.get_item(
                TableName=os.environ['RECIPIENTS_TABLE'],
                Key={
                    'recipientId': {'S': recipient_id}
                }
            )

            if 'Item' not in resp:
                return generate_response(400, {
                    "success": False,
                    "message": "This fire invite does not exist for you"
                })

            fire_id = resp.get('Item').get("fireId").get("S")

            # Get chat id from fires, check if fire exists
            response = client_db.get_item(
                TableName=os.environ['FIRES_TABLE'],
                Key={
                    'fireId': {'S': fire_id}
                }
            )

            if 'Item' not in response:
                return generate_response(400, {
                    "success": False,
                    "message": "This fire does not exist"
                })

            chat_id = response.get('Item').get("chatId").get("S")

            add_chat_user(current_user, chat_id)

        # Delete original invite
        client_db.delete_item(
            TableName=os.environ['RECIPIENTS_TABLE'],
            Key={
                'recipientId': {'S': recipient_id}
            }
        )

        return generate_response(200, {
            "success": True
        })

    except Exception as e:
        return handle_exception(e)
