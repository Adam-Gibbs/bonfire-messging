import boto3
from helpers.returns import generate_response
from helpers.getRequestData import get_body, check_fields
import helpers.config as config
from auth.authExceptions import handle_auth_exception


def lambda_handler(event, context):
    params = get_body(event)

    invalid_fields = check_fields(
        ["username", "email", "password"],
        [str, str, str],
        event
    )
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    email = params["email"]
    password = params['password']

    client_cognito = boto3.client('cognito-idp')

    try:
        client_cognito.sign_up(
            ClientId=config.CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': "username",
                    'Value': username
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "username",
                    'Value': username
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ]
        )

    except client_cognito.exceptions.UsernameExistsException as e:
        print("UsernameExistsException")
        print(e)
        return generate_response(400, {
            "success": False,
            "message": "This username already exists"
        })

    except client_cognito.exceptions.InvalidPasswordException as e:
        print("InvalidPasswordException")
        print(e)
        return generate_response(400, {
            "success": False,
            "message": "Password should have Caps, Lower cas and Numbers"
        })

    except client_cognito.exceptions.UserLambdaValidationException as e:
        print("UserLambdaValidationException")
        print(e)
        return generate_response(400, {
            "success": False,
            "message": "Email already exists"
        })

    except Exception as e:
        return handle_auth_exception(e)

    return generate_response(200, {
        "success": True,
        "message": "Please confirm your signup, check Email for"
                   "validation code",
    })
