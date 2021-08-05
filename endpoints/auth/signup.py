import base64
import hashlib
import hmac
import json

import boto3
import botocore.exceptions

USER_POOL_ID = 'eu-west-2_xUNInjJwa'
CLIENT_ID = '8gjhsrum4alfi1u9i6prargi2'
# CLIENT_SECRET = ''

# def get_secret_hash(username):
# 	msg = username + CLIENT_ID
# 	dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
# 		msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()

# 	d2 = base64.b64encode(dig).decode()
# 	return d2


def lambda_handler(event, context):
    for field in ["username", "email", "password", "name"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"{field} is not present", "data": None}

    username = event['username']
    email = event["email"]
    password = event['password']
    name = event["name"]

    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
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

        print(resp)
    except client.exceptions.UsernameExistsException as e:
        return {
            "success": False,
            "message": "This username already exists",
            "data": None
        }

    except client.exceptions.InvalidPasswordException as e:
        return {
            "success": False,
            "message": "Password should have Caps,\
						Special chars, Numbers",
            "data": None
        }

    except client.exceptions.UserLambdaValidationException as e:
        return {
            "success": False,
            "message": "Email already exists",
            "data": None
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "data": None
        }

    return {
        "success": True,
        "message": "Please confirm your signup, \
					check Email for validation code",
    }
