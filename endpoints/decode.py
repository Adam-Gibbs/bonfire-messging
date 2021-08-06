import cognitojwt
from endpoints.helpers.getData import get_header_auth
from endpoints.helpers.returns import generate_response
import endpoints.helpers.config as config


def decode_token(token):
    return cognitojwt.decode(
        token,
        config.USER_POOL_LOC,
        config.USER_POOL_ID,
        app_client_id=config.CLIENT_ID
    )



def lambda_handler(event, context):
    return generate_response(200, {
        "data": decode_token(get_header_auth(event))
    })
