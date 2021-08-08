import boto3

import endpoints.helpers.config as config


def get_email(username):
    client_cognito = boto3.client('cognito-idp')

    resp = client_cognito.list_users(
        AttributesToGet=["email"],
        Filter=f'username = "{username}"',
        Limit=1,
        UserPoolId=config.USER_POOL_ID
    )

    return resp["Users"][0]["Attributes"][0]["Value"]
