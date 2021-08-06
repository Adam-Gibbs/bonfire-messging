import json
from endpoints.helpers.returns import generate_response


def get_body(event):
    return json.loads(event.get("body"))


def get_path(event):
    return event.get("pathParameters")


def get_header(event):
    return event.get("header")
    

def get_user(event):
    return event.get("pathParameters")


def required_fields(fields, event):
    body = get_body(event)
    for field in fields:
        if body.get(field) is None:
            return generate_response(400, {
                "success": False,
                "message": f"{field} is required",
            })

    return None
