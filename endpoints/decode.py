import requests
from jose import jwt
from pprint import pprint
from endpoints.helpers.getData import get_header_auth
from endpoints.helpers.returns import generate_response
import endpoints.helpers.config as config


def decode_token(token):
    return jwt.decode(token)


def lambda_handler(event, context):
    return generate_response(200, {
        "data": decode_token(get_header_auth(event))
    })
