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

    invalid_fields = required_fields(["username", "message"], event)
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    message = params['message']

    try:
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
            "success": True
        })

    except Exception as e:
        return handle_exception(e)
