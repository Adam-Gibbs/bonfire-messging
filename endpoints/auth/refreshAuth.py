import boto3

from endpoints.helpers.returns import generate_response
from endpoints.helpers.getRequestData import get_body, check_fields
import endpoints.helpers.config as config
import authExceptions


def lambda_handler(event, context):
    params = get_body(event)
    client_cognito = boto3.client('cognito-idp')

    invalid_fields = check_fields(
        ["username", "refresh_token"],
        [str, str],
        event
    )
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    refresh_token = params["refresh_token"]

    try:
        resp = client_cognito.initiate_auth(
            AuthParameters={
                    'USERNAME': username,
                    'REFRESH_TOKEN': refresh_token
            },
            ClientId=config.CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
        )
        res = resp.get("AuthenticationResult")

    except client_cognito.exceptions.NotAuthorizedException:
        return generate_response(400, {
            "success": False,
            "message": "Invalid refresh token"
        })

    except Exception as e:
        return authExceptions.handle_auth_exception(e)

    try:
        return generate_response(200, {
            "success": True,
            'message': "success",
            "data": {
                "id_token": res["IdToken"],
                "access_token": res["AccessToken"],
                "expires_in": res["ExpiresIn"],
                "token_type": res["TokenType"]
            }
        })

    except Exception as e:
        return authExceptions.handle_auth_exception(e)
