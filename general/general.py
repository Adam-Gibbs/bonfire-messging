try:
    import os
    import json
    import boto3

except ImportError:
    # Deal with this
    pass

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
            'userId': { 'S': event.get("pathParameters").get("user_id") }
        }
    )
    item = resp.get('Item')
    if not item:
        print('error')
        return {
            'statusCode': 404,
            'error': 'User does not exist'
        }

    print('good')
    return {
        'statusCode': 200,
        'body': {
            'userId': item.get('userId').get('S'), 
            'name': item.get('name').get('S')
        }
    }

def create_user(event, context):
    json_body = json.loads(event.get("body"))
    user_id = json_body.get('userId')
    name = json_body.get('name')
    if not user_id or not name:
        print('error')
        return {
            'statusCode': 400,
            'error': 'Please provide userId and name'
        }

    client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )

    print('good')
    return {
        'statusCode': 200,
        'body': user_id,
    }