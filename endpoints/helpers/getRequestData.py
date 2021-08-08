import json
from endpoints.helpers.returns import generate_response


def get_body(event):
    return json.loads(event.get("body"))


def get_path(event):
    return event.get("pathParameters")


def get_header_auth(event):
    return event.get("headers").get("Authorization")


def check_fields(fields, types, event, optional_fields=[], optional_types=[]):
    body = get_body(event)
    print(body)
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

    for index, optional_field in enumerate(optional_fields):
        if body.get(optional_field) is not None and \
           type(body.get(optional_field)) is not optional_types[index]:
            return generate_response(400, {
                "success": False,
                "message":
                    f"{optional_field} is required " +
                    f"to be type {optional_types[index]}",
            })

    return None
