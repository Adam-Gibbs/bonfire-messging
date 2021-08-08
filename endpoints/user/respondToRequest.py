from endpoints.helpers.getRequestData import get_body, required_fields
from endpoints.user_methods.getUsername import get_username
from endpoints.helpers.returns import generate_response
from endpoints.exceptions import handle_exception
import boto3
import os


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = required_fields(["friendRequestId", "accepted"], event)
    if invalid_fields is not None:
        return invalid_fields

    friend_request_id = params['friendRequestId']
    accepted = params['accepted']
    print(f"friend_request_id: {friend_request_id}, accepted: {accepted}")

    try:
        if accepted is True:
            resp = client_db.get_item(
                TableName=os.environ['FRIEND_REQUESTS_TABLE'],
                Key={
                    'friendRequestId': {'S': friend_request_id}
                }
            )

            print(resp)
            other_user = resp.get('Items').get("requestFrom")
            print(other_user)

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

        return generate_response(200, {
            "success": True
        })

    except Exception as e:
        return handle_exception(e)
