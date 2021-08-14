import os

import boto3


def get_all_chat_ids(user):
    client_db = boto3.client('dynamodb')

    resp = client_db.query(
        TableName=os.environ['CHAT_MEMBERS_TABLE'],
        IndexName='chatMember-index',
        KeyConditionExpression='chatMember = :user',
        ExpressionAttributeValues={
            ':user': {'S': user}
        }
    )

    total = []
    if 'Items' in resp:
        for item in resp.get("Items"):
            total.append(item.get("chatId").get("S"))

    return total


def get_chats(user):
    client_db = boto3.client('dynamodb')

    chats = get_all_chat_ids(user)

    total = []
    for chat_id in chats:
        resp = client_db.query(
            TableName=os.environ['CHATS_TABLE'],
            KeyConditionExpression='chatId = :user',
            ExpressionAttributeValues={
                ':user': {'S': chat_id}
            }
        )

        if 'Items' in resp:
            total.extend(resp.get("Items"))

    return total
