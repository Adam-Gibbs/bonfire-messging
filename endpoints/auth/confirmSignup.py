import boto3

from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, required_fields
import endpoints.helpers.config as config
import authExceptions


def lambda_handler(event, context):
    params = get_body(event)
    client = boto3.client('cognito-idp')

    invalid_fields = required_fields(["username", "code"], event)
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    code = params['code']

    try:
        client.confirm_sign_up(
            ClientId=config.CLIENT_ID,
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )

    except client.exceptions.NotAuthorizedException:
        print("NotAuthorizedException")
        return generate_response(400, {
            "success": False,
            "message": "User is already confirmed"
        })

    except Exception as e:
        return authExceptions.handle_auth_exception(e)

    return generate_response(200, {
        "success": True,
        "message": "Your account is now verified"
    })
