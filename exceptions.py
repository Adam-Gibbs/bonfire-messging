from helpers.returns import generate_response


def handle_exception(exception):
    name = type(exception).__name__

    if name == "JSONDecodeError":
        print("JSONDecodeError")
        print(exception)
        return generate_response(400, {
            "success": False,
            "message": "The request you have provided is invalid"
        })

    print(f"Else Exception: {exception}")
    return generate_response(400, {
            "success": False,
            "message": f"Unknown error {exception.__str__()} "
        })
