from helpers.getRequestData import get_header_auth
from user_methods.decode import decode_token


def get_username(event):
    header_data = get_header_auth(event)
    return decode_token(header_data).get("username")
