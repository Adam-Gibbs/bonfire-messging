from endpoints.user_methods.checkFriends import check_friends
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)

    try:
        return generate_response(200,  {
            "friends": check_friends(current_user)
        })

    except Exception as e:
        return handle_exception(e)
