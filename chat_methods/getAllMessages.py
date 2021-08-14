import os

import boto3


def get_all_messages(chat_id, time):
    client_db = boto3.client('dynamodb')
    resp = client_db.query(
        TableName=os.environ['MESSAGES_TABLE'],
        IndexName='chatId-sent-index',
        KeyConditionExpression='chatId = :chat_id AND sent > :sent',
        ExpressionAttributeValues={
            ':chat_id': {'S': chat_id},
            ':sent': {'S': str(time)}
        }
    )

    resp_items = []
    if 'Items' in resp:
        resp_items = resp.get("Items")

    return resp_items
