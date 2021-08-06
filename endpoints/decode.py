import requests
from jose import jwt
from pprint import pprint
from endpoints.helpers.getData import get_header_auth
from endpoints.helpers.returns import generate_response
import endpoints.helpers.config as config


def decode_token(token):
    jwks_url = 'https://cognito-idp.{}.amazonaws.com/{}/' \
                '.well-known/jwks.json'.format(
                        config.USER_POOL_LOC,
                        config.USER_POOL_ID)
    jwks = requests.get(jwks_url).json()
    pprint(jwt.decode(token, jwks))


def lambda_handler(event, context):
    return generate_response(200, {
        "data": decode_token(get_header_auth(event))
    })
