from endpoints.helpers.returns import generate_response
import endpoints.exceptions


def handle_auth_exception(exception):
    name = type(exception).__name__
    print(f"Exception name: {name}")

    if name == "NotAuthorizedException":
        print("NotAuthorizedException")
        return generate_response(400, {
            "success": False,
            "message": "The username or password is incorrect"
        })

    if name == "UserNotConfirmedException":
        print("UserNotConfirmedException")
        return generate_response(400, {
            "success": False,
            "message": "User is not confirmed"
        })

    if name == "CodeMismatchException":
        print("CodeMismatchException")
        return generate_response(400, {
            "success": False,
            "message": "Invalid Verification code"
        })

    if name == "UserNotFoundException":
        print("UserNotFoundException")
        return generate_response(400, {
            "success": False,
            "message": "Username does not exists"
        })

    else:
        return endpoints.exceptions.handle_exception(exception)
