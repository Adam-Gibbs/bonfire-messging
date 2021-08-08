import os

import boto3
import endpoints.helpers.config as config
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)
    client_db = boto3.client('dynamodb',  region_name=config.USER_POOL_LOC)

    try:
        resp1 = client_db.query(
            TableName=os.environ['FRIENDS_TABLE'],
            KeyConditionExpression='friendTo = :currentUser',
            ExpressionAttributeValues={
                ':currentUser': {'S': current_user}
            }
        )

        resp2 = client_db.query(
            TableName=os.environ['FRIENDS_TABLE'],
            KeyConditionExpression='friendTo = :currentUser',
            ExpressionAttributeValues={
                ':currentUser': {'S': current_user}
            }
        )

        if 'Items' in resp1:
            resp1_items = resp1.get("Items")
        else:
            resp1_items = {}

        if 'Items' in resp2:
            total = resp2.get("Items")
        else:
            total = {}

        total.append(resp1_items)

        return generate_response(200,  {
            "resp": total
        })

    except Exception as e:
        return handle_exception(e)
