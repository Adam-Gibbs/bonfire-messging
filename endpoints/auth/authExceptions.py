from endpoints.helpers.returns import generate_response
import exceptions


def handle_auth_exception(exception):
    name = type(exception).__name__

    if name == "NotAuthorizedException":
        return generate_response(400, {
            "success": False,
            "message": "The username or password is incorrect"
        })

    if name == "UserNotConfirmedException":
        return generate_response(400, {
            "success": False,
            "message": "User is not confirmed"
        })

    if name == "CodeMismatchException":
        return generate_response(400, {
            "success": False,
            "message": "Invalid Verification code"
        })

    if name == "client.exceptions.UserNotFoundException":
        return generate_response(400, {
            "success": False,
            "message": "Username does not exists"
        })

    else:
        return exceptions.handle_exception(exception)
