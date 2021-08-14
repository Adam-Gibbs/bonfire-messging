import os
import time

import boto3
from chat_methods.createChat import create_chat
from exceptions import handle_exception
from geopy.geocoders import Nominatim
from helpers.getRequestData import check_fields, get_body, validate_dict
from helpers.returns import generate_response
from helpers.uniqueKey import unique_key
from user_methods.checkFriends import check_friends
from user_methods.getUsername import get_username


def get_location_name(lat, long):
    geo = Nominatim(user_agent="GetLoc")
    location_name = geo.reverse(f"{lat}, {long}")
    if location_name is None:
        return 'Unknown, Unknown'
    location_name = location_name.address.split(",")

    if len(location_name) == 1:
        return f'Unknown, {location_name[0]}'

    if len(location_name) == 2:
        return f'{location_name[0]}, {location_name[1]}'

    if len(location_name) > 2:
        return f'{location_name[1]}, {location_name[2]}'


def check_recipients(public, recipients, user):
    if not public and len(recipients) < 1:
        return generate_response(400, {
                "success": False,
                "message": "Your private chat does "
                           "not specify any recipients"
            })

    if public and len(recipients) > 0:
        return generate_response(400, {
                "success": False,
                "message": "Your public chat can "
                           "not specify any recipients"
            })

    if public and user in recipients:
        return generate_response(400, {
                "success": False,
                "message": "Your recipients can not include yourself"
            })

    friends = check_friends(user)
    for recipient in recipients:
        if recipient not in friends:
            return generate_response(400, {
                "success": False,
                "message": f"You are not friends with {recipient}"
            })

    return None


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["message", "location", "public"],
        [str, dict, bool],
        event,
        ["recipients"],
        [list]
    )
    if invalid_fields is not None:
        return invalid_fields

    message = params['message']
    location = params['location']
    public = params['public']
    recipients = []
    if "recipients" in params:
        recipients = params["recipients"]

    invalid_dict = validate_dict(
        "location",
        location,
        ["lat", "long"],
        [float, float]
    )
    if invalid_dict is not None:
        return invalid_dict

    invalid_recipients = check_recipients(public, recipients, current_user)
    if invalid_recipients is not None:
        return invalid_recipients

    try:
        fire_id = str(
            unique_key(current_user, os.environ['FIRES_TABLE'], 'fireId')
        )
        location_name = get_location_name(location['lat'], location['long'])
        chat_id = create_chat(current_user, fire_id, "")

        client_db.put_item(
            TableName=os.environ['FIRES_TABLE'],
            Item={
                'fireId': {'S': fire_id},
                'creator': {'S': current_user},
                'lat': {'S': str(location["lat"])},
                'long': {'S': str(location["long"])},
                'location': {'S': location_name},
                'publicFire': {'S': str(public)},
                'message': {'S': message},
                'created': {'S': str(time.time())},
                'chatId': {'S': chat_id}
            }
        )

        for recipient in recipients:
            client_db.put_item(
                TableName=os.environ['RECIPIENTS_TABLE'],
                Item={
                    'recipientId': {'S': (fire_id + recipient)},
                    'fireId': {'S': fire_id},
                    'username': {'S': recipient}
                }
            )

        return generate_response(200, {
            "success": True,
            "message": "Fire created"
        })

    except Exception as e:
        return handle_exception(e)
