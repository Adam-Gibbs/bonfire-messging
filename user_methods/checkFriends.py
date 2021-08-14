import os

import boto3


def get_all_friends(list, section):
    total = []
    for friend in list:
        total.append(friend.get(section).get("S"))

    return total


def check_friends(user):
    client_db = boto3.client('dynamodb')

    resp1 = client_db.query(
        TableName=os.environ['FRIENDS_TABLE'],
        IndexName='friendTo-index',
        KeyConditionExpression='friendTo = :currentUser',
        ExpressionAttributeValues={
            ':currentUser': {'S': user}
        }
    )

    resp2 = client_db.query(
        TableName=os.environ['FRIENDS_TABLE'],
        IndexName='friendOf-index',
        KeyConditionExpression='friendOf = :currentUser',
        ExpressionAttributeValues={
            ':currentUser': {'S': user}
        }
    )

    if 'Items' in resp1:
        resp1_items = get_all_friends(resp1.get("Items"), 'friendOf')
    else:
        resp1_items = []

    if 'Items' in resp2:
        total = get_all_friends(resp2.get("Items"), 'friendTo')
    else:
        total = []

    total.extend(resp1_items)

    return total
