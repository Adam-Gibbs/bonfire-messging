import os

import boto3
import endpoints.helpers.config as config
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb',  region_name=config.USER_POOL_LOC)
    query = 'friendTo = :currentUser OR friendOf = :currentUser'

    try:
        resp = client_db.query(
            TableName=os.environ['FRIENDS_TABLE'],
            KeyConditionExpression=query,
            ExpressionAttributeValues={
                ':currentUser': {'S': current_user}
            }
        )

        return generate_response(200,  {
            "resp": resp.get('Items')
        })

    except Exception as e:
        return handle_exception(e)
