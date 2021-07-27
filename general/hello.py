try:
    import os
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

def handler(event, context):
    return {
        'statusCode': 200,
        'body':"Hello World!"
    }