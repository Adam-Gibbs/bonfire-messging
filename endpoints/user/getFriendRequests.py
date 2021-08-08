import os

from dynamof.operations import query
from dynamof.conditions import attr
from endpoints.exceptions import handle_exception
from endpoints.helpers.returns import generate_response
from endpoints.user_methods.getUsername import get_username


def lambda_handler(event, context):
    current_user = get_username(event)

    try:
        resp = query(
            table_name=os.environ['FRIEND_REQUESTS_TABLE'],
            conditions=attr('to').equals(current_user),
            index_name='to-index'
        )

        print(resp)
        print("\n")
        print(resp.get('Items'))

        generate_response(200,  {
            "resp": resp
        })

    except Exception as e:
        return handle_exception(e)
