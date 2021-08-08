import os
import boto3


def check_friends(user):
    client_db = boto3.client('dynamodb')

    resp1 = client_db.query(
        TableName=os.environ['FRIENDS_TABLE'],
        KeyConditionExpression='friendTo = :currentUser',
        ExpressionAttributeValues={
            ':currentUser': {'S': user}
        }
    )

    resp2 = client_db.query(
        TableName=os.environ['FRIENDS_TABLE'],
        KeyConditionExpression='friendTo = :currentUser',
        ExpressionAttributeValues={
            ':currentUser': {'S': user}
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

    return total
