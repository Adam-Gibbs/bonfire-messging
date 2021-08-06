import os
import json
import boto3

from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, get_path

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')

def get_user(event, context):
    params = get_path(event)
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': params.get("user_id") }
        }
    )
    item = resp.get('Item')
    if not item:
        return generate_response(404, {
            'error': 'User does not exist'
        })

    return generate_response(200,
        {
            'userId': item.get('userId').get('S'),
            'name': item.get('name').get('S')
        }
    )

def create_user(event, context):
    json_body = get_body(event)
    user_id = json_body.get('userId')
    name = json_body.get('name')
    if not user_id or not name:
        return generate_response(400, {
            'error': 'Please provide userId and name'
        })

    client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )

    return generate_response(200,
        {
            'userId': user_id,
            'name': name
        }
    )