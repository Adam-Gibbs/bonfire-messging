import boto3

import endpoints.auth.authExceptions as authExceptions
import endpoints.helpers.config as config


def get_email(username):
    client_cognito = boto3.client('cognito-idp')

    try:
        client_cognito.list_users(
            AttributesToGet=["email"],
            Filter=f'username = "{username}"',
            Limit=1,
            UserPoolId=config.config.USER_POOL_ID
        )

    except Exception as e:
        return authExceptions.handle_auth_exception(e)
