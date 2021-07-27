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

def handler(event, context):
    return {
        'statusCode': 200,
        'body':"Hello World!"
    }