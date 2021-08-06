from endpoints.helpers.returns import generate_response


def handle_auth_exception(exception):
    name = type(exception).__name__

    return generate_response(400, {
            "success": False,
            "message": f"Unknown error {exception.__str__()} "
        })
