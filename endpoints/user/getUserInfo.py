from endpoints.user_methods.getUsername import get_username
from endpoints.user_methods.getEmail import get_email
from endpoints.helpers.returns import generate_response
from endpoints.auth.authExceptions import handle_auth_exception


def lambda_handler(event, context):
    try:
        username = get_username(event)
        email = get_email(username)

        return generate_response(200, {
            "username": username,
            "email": email
        })

    except Exception as e:
        return handle_auth_exception(e)
