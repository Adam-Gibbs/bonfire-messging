import boto3
from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, required_fields
import endpoints.helpers.config


def lambda_handler(event, context):
    params = get_body(event)

    required_fields(["username", "email", "password"])
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
        return generate_response(400, {
            "success": False,
            "message": "This username already exists"
        })

    except client.exceptions.InvalidPasswordException:
        return generate_response(400, {
            "success": False,
            "message": "Password should have Caps, Special chars, Numbers"
        })

    except client.exceptions.UserLambdaValidationException:
        return generate_response(400, {
            "success": False,
            "message": "Email already exists"
        })

    except Exception as e:
        return generate_response(400, {
            "success": False,
            "message": str(e)
        })

    return generate_response(200, {
        "success": True,
        "message": "Please confirm your signup, check Email for"
                   "validation code",
    })
