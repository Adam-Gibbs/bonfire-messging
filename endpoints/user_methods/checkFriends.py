import os
import boto3


def get_all_friends(list, section):
    total = []
    for friend in list:
        print(friend)
        total.append(friend.get(section))

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
        resp1_items = get_all_friends(resp1, 'friendOf')
    else:
        resp1_items = []

    if 'Items' in resp2:
        total = get_all_friends(resp2, 'friendTo')
    else:
        total = []

    total.append(resp1_items)

    return total
