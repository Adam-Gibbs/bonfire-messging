import json
from base64 import urlsafe_b64decode


def maybe_pad(s):
    return (s + '=' * (4 - len(s) % 4))


def decode_token(token):
    _, payload, _ = token.split(".")
    payload_json_str = urlsafe_b64decode(maybe_pad(payload))
    payload_json = json.loads(payload_json_str)

    return {
        "username": payload_json["username"],
        "email": payload_json["email"]
    }
