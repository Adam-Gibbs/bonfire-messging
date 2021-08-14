import json

from helpers.returns import generate_response


def get_body(event):
    return json.loads(event.get("body"))


def get_path(event):
    return event.get("pathParameters")


def get_header_auth(event):
    return event.get("headers").get("Authorization")


def validate_dict(field_name, dictionary, expected_keys, expected_types):
    keys = dictionary.keys()

    if set(keys) != set(expected_keys):
        return generate_response(400, {
                "success": False,
                "message": f"{field_name} did not follow the required "
                           f"format, provide only {expected_keys}",
            })

    # Checks each expected key matches the expected type
    for index in range(len(dictionary)):
        if type(dictionary.get(expected_keys[index])) is not \
                expected_types[index]:
            return generate_response(400, {
                    "success": False,
                    "message": f"{expected_keys[index]} should be "
                               f"of type {expected_types[index]}",
                })


def check_fields(fields, types, event, optional_fields=[], optional_types=[]):
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

    for index, optional_field in enumerate(optional_fields):
        if body.get(optional_field) is not None and \
           type(body.get(optional_field)) is not optional_types[index]:
            return generate_response(400, {
                "success": False,
                "message":
                    f"{optional_field} is required " +
                    f"to be type {optional_types[index]}",
            })

    for key in body.keys():
        if key not in fields and key not in optional_fields:
            return generate_response(400, {
                "success": False,
                "message": f"Too many fields, {key} is not required ",
            })

    return None
