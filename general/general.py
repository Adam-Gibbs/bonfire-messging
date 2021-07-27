try:
    import os
    import json
    import boto3
    from flask import Flask, jsonify, request

except ImportError:
    # Deal with this
    pass

app = Flask(__name__)

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
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': event.pathParameters.user_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })

def create_user(event, context):
    print(event)
    # user_id = request.json.get('userId')
    # name = request.json.get('name')
    # if not user_id or not name:
    #     return jsonify({'error': 'Please provide userId and name'}), 400

    # client.put_item(
    #     TableName=USERS_TABLE,
    #     Item={
    #         'userId': {'S': user_id },
    #         'name': {'S': name }
    #     }
    # )

    # return {
    #     'userId': user_id,
    #     'name': name
    # }