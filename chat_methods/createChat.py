import os
import time

import boto3
from helpers.uniqueKey import unique_key
from chat_methods.addChatUser import add_chat_user


def create_chat(user, fire_id, user_2=None):
    client_db = boto3.client('dynamodb')

    unique = str(unique_key(
        user,
        os.environ['CHATS_TABLE'],
        'chatId'
    ))

    client_db.put_item(
        TableName=os.environ['CHATS_TABLE'],
        Item={
            'chatId': {'S': unique},
            'fireId': {'S': str(fire_id)},
            'created': {'S': str(time.time())},
            'createdBy': {'S': user}
        }
    )

    add_chat_user(user, unique)

    if user_2 is not None:
        add_chat_user(user_2, unique)

    return unique
