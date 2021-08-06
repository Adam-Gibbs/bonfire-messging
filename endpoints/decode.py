import requests
from jose import jwt
from pprint import pprint
from endpoints.helpers.getData import get_header
import endpoints.helpers.config as config


def decode_token(token):
    # build the URL where the public keys are
    jwks_url = 'https://cognito-idp.{}.amazonaws.com/{}/' \
                '.well-known/jwks.json'.format(
                        config.USER_POOL_LOC,
                        config.USER_POOL_ID)
    # get the keys
    jwks = requests.get(jwks_url).json()
    pprint(jwt.decode(token, jwks))


def lambda_handler(event, context):
    pprint(event)
    pprint(get_header(event))
