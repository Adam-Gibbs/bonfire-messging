import boto3
from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, required_fields
import endpoints.helpers.config
import authExceptions


def lambda_handler(event, context):
    params = get_body(event)

    invalid_fields = required_fields(["username", "email", "password"], event)
    if invalid_fields is not None:
        return invalid_fields

    username = params['username']
    email = params["email"]
    password = params['password']

    client = boto3.client('cognito-idp')

    try:
        client.sign_up(
            ClientId=endpoints.helpers.config.CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                },
                {
                    'Name': "custom:username",
                    'Value': username
                }
            ]
        )

    except client.exceptions.UsernameExistsException:
        print("UsernameExistsException")
        return generate_response(400, {
            "success": False,
            "message": "This username already exists"
        })

    except client.exceptions.InvalidPasswordException:
        print("InvalidPasswordException")
        return generate_response(400, {
            "success": False,
            "message": "Password should have Caps, Lower cas and Numbers"
        })

    except client.exceptions.UserLambdaValidationException:
        print("UserLambdaValidationException")
        return generate_response(400, {
            "success": False,
            "message": "Email already exists"
        })

    except Exception as e:
        return authExceptions.handle_auth_exception(e)

    return generate_response(200, {
        "success": True,
        "message": "Please confirm your signup, check Email for"
                   "validation code",
    })
