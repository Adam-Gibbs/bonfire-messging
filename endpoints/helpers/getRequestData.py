import json
from endpoints.helpers.returns import generate_response


def get_body(event):
    return json.loads(event.get("body"))


def get_path(event):
    return event.get("pathParameters")


def get_header_auth(event):
    return event.get("headers").get("Authorization")


def check_fields(fields, types, event):
    body = get_body(event)
    for index, field in enumerate(fields):
        if body.get(field) is None:
            return generate_response(400, {
                "success": False,
                "message": f"{field} is required",
            })

        if type(body.get(field)) is not types[index]:
            return generate_response(400, {
                "success": False,
                "message": f"{field} is required to be type {types[index]}",
            })

    return None
