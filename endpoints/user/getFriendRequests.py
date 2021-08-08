from endpoints.user_methods.getUsername import get_username
from endpoints.helpers.returns import generate_response
from endpoints.exceptions import handle_exception
import boto3
import os


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    try:
        resp = client_db.get_item(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            Key={
                'to-index': {'S': current_user}
            }
        )

        print(resp)

        generate_response(200,  {
            "resp": resp
        })

    except Exception as e:
        return handle_exception(e)
