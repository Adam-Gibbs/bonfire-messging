from endpoints.user_methods.getUsername import get_username
from endpoints.user_methods.getEmail import get_email
from helpers.returns import generate_response


def lambda_handler(event, context):
    username = get_username(event)
    email = get_email(username)

    return generate_response(200, {
        "username": username,
        "email": email
    })
