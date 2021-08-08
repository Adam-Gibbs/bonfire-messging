import os

import boto3
from boto3.dynamodb.conditions import Key
import endpoints.helpers.config as config
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb',  region_name=config.USER_POOL_LOC)

    try:
        resp = client_db.query(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            KeyConditionExpression=Key('to').eq(current_user)
        )

        print(resp)
        print("\n")
        print(resp.get('Items'))

        generate_response(200,  {
            "resp": resp
        })

    except Exception as e:
        return handle_exception(e)
