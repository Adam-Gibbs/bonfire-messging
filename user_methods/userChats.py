import os

import boto3


def get_all_chat_ids(user):
    chats = get_chats(user)
    total = []

    for item in chats:
        total.append(item.get("chatId").get("S"))

    return total


def get_chats(user):
    client_db = boto3.client('dynamodb')

    resp = client_db.query(
        TableName=os.environ['CHAT_MEMBERS_TABLE'],
        IndexName='chatMember-index',
        KeyConditionExpression='chatMember = :user',
        ExpressionAttributeValues={
            ':user': {'S': user}
        }
    )

    chats = []
    if 'Items' in resp:
        chats = resp.get("Items")

    return chats


def chat_has_user(chat_id, user):
    chats = get_chats(user)
    total = []

    for item in chats:
        total.append(item.get("chatId").get("S"))

    return chat_id in total
