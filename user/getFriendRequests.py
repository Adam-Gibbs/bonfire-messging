import os

import boto3
import helpers.config as config
from exceptions import handle_exception
from helpers.returns import generate_response
from user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb',  region_name=config.USER_POOL_LOC)

    try:
        resp = client_db.query(
            TableName=os.environ['FRIEND_REQUESTS_TABLE'],
            IndexName='requestTo-index',
            KeyConditionExpression='requestTo = :requestTo',
            ExpressionAttributeValues={
                ':requestTo': {'S': current_user}
            }
        )

        return generate_response(200,  {
            "resp": resp.get('Items')
        })

    except Exception as e:
        return handle_exception(e)
