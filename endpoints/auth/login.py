import boto3

from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, required_fields
import endpoints.helpers.config
import authExceptions


def initiate_auth(client, username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=endpoints.helpers.config.USER_POOL_ID,
            ClientId=endpoints.helpers.config.CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            }
        )

    except Exception as e:
        return None, authExceptions.handle_exception(e)

    return resp, None


def lambda_handler(event, context):
    params = get_body(event)
    client = boto3.client('cognito-idp')

    required_fields(["username", "password"])
    username = params['username']
    password = params['password']

    resp, err = initiate_auth(client, username, password)
    if err is not None:
        return err

    if resp.get("AuthenticationResult"):
        return generate_response(200, {
            "success": True,
            "message": "Success",
            "data": {
                "id_token": resp["AuthenticationResult"]["IdToken"],
                "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                "token_type": resp["AuthenticationResult"]["TokenType"]
            }
        })

    else:  # this code block is relevant only when MFA is enabled
        generate_response(200, {
            "success": False,
            "message": "MFA has failed"
        })
