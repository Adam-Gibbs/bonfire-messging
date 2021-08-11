import os
from re import T

import boto3
from endpoints.auth.authExceptions import handle_auth_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    try:
        current_user = get_username(event)
        client_db = boto3.client('dynamodb')

        public_fires = client_db.query(
            TableName=os.environ['FIRES_TABLE'],
            IndexName='publicFire-index',
            KeyConditionExpression='publicFire = :publicFire',
            ExpressionAttributeValues={
                ':publicFire': {'S': "True"}
            }
        )

        if 'Items' in public_fires:
            public_fires = public_fires.get("Items")
        else:
            public_fires = []

        invited = client_db.query(
            TableName=os.environ['RECIPIENTS_TABLE'],
            IndexName='username-index',
            KeyConditionExpression='username = :current_user',
            ExpressionAttributeValues={
                ':current_user': {'S': current_user}
            }
        )

        invited_fires = []

        if 'Items' in invited:
            for item in invited.get("Items"):
                invited_fires.append(
                    client_db.get_item(
                        TableName=os.environ['FIRES_TABLE'],
                        Key={
                            'fireId': {'S': item["fireId"]["S"]}
                        }
                    )
                )

        return generate_response(200, {
            "public": public_fires,
            "invited": invited_fires,
        })

    except Exception as e:
        return handle_auth_exception(e)
