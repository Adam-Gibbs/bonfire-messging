import boto3

from endpoints.helpers.returns import generate_response
from endpoints.helpers.getData import get_body, required_fields
import endpoints.helpers.config
import authExceptions


def lambda_handler(event, context):
    params = get_body(event)
    client = boto3.client('cognito-idp')

    invalid_fields = required_fields(["username"], event)
    if invalid_fields is not None:
        return invalid_fields

    try:
        username = params['username']
        client.resend_confirmation_code(
            ClientId=endpoints.helpers.config.CLIENT_ID,
            Username=username,
        )

    except client.exceptions.InvalidParameterException:
        print("InvalidParameterException")
        return generate_response(400, {
                "success": False,
                "message": "User is already confirmed"
            })

    except Exception as e:
        return authExceptions.handle_auth_exception(e)

    return generate_response(200, {
        "success": True
    })
