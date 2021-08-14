from exceptions import handle_exception
from user_methods.getUsername import get_username
from user_methods.userChats import get_chats
from helpers.returns import generate_response


def lambda_handler(event, context):
    try:
        current_user = get_username(event)
        chats = get_chats(current_user)

        return generate_response(200, {
            "success": True,
            "chats": chats,
        })

    except Exception as e:
        return handle_exception(e)
