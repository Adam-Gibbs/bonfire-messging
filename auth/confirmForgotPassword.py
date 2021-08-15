import boto3

from helpers.returns import generate_response
from helpers.getRequestData import get_body, check_fields
import helpers.config as config
from auth.authExceptions import handle_auth_exception


def lambda_handler(event, context):
    params = get_body(event)
    client_cognito = boto3.client('cognito-idp')

    invalid_fields = check_fields(
        ["username", "new-password", "code"],
        [str, str, str],
        event
    )
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    password = params['new-password']
    code = params['code']

    try:
        client_cognito.confirm_forgot_password(
                ClientId=config.CLIENT_ID,
                Username=username,
                ConfirmationCode=code,
                Password=password,
           )

    except client_cognito.exceptions.NotAuthorizedException as e:
        print("NotAuthorizedException")
        print(e)
        return generate_response(400, {
            "success": False,
            "message": "User is already confirmed"
        })

    except Exception as e:
        return handle_auth_exception(e)

    return generate_response(200, {
        "success": True,
        "message": "Password has been changed successfully",
    })
