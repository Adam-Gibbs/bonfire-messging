import os

import boto3


def add_chat_user(user, chat_id):
    client_db = boto3.client('dynamodb')

    client_db.put_item(
        TableName=os.environ['CHAT_MEMBERS_TABLE'],
        Item={
            'chatMemberId': {'S': user+chat_id},
            'chatId': {'S': chat_id},
            'chatMember': {'S': user},
        }
    )
