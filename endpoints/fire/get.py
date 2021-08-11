import os

import boto3
from geopy import distance
from endpoints.exceptions import handle_exception
from endpoints.helpers.getRequestData import check_fields, get_body, \
                                             validate_dict
from endpoints.user_methods.getUsername import get_username
from endpoints.helpers.returns import generate_response


def lambda_handler(event, context):
    params = get_body(event)
    current_user = get_username(event)
    client_db = boto3.client('dynamodb')

    invalid_fields = check_fields(
        ["location", "distance"],
        [dict, int],
        event,
        ["public"],
        [bool]
    )
    if invalid_fields is not None:
        return invalid_fields

    invalid_dict = validate_dict(
        "location",
        params['location'],
        ["lat", "long"],
        [float, float]
    )
    if invalid_dict is not None:
        return invalid_dict

    location = (params['location']['lat'], params['location']['long'])
    distance_km = params['distance']
    public = None
    if "public" in params:
        public = params["public"]

    if distance_km > 100:
        return generate_response(400, {
            "success": False,
            "message": "You cannot search a distance greater than 100km",
        })

    try:
        current_user = get_username(event)
        client_db = boto3.client('dynamodb')

        public_fires = []
        if public is not False:
            public_fires = client_db.query(
                TableName=os.environ['FIRES_TABLE'],
                IndexName='publicFire-index',
                KeyConditionExpression='publicFire = :publicFire',
                ExpressionAttributeValues={
                    ':publicFire': {'S': "True"}
                }
            )

            if 'Items' in public_fires:
                # If public chat is within requested distance, added to list
                for item in public_fires.get("Items"):
                    point_location = (float(item['lat']), float(item['long']))
                    if (
                        distance.distance(location, point_location).km
                            <= distance_km):
                        public_fires.append(item)

        invited_fires = []
        if public is not True:
            invited = client_db.query(
                TableName=os.environ['RECIPIENTS_TABLE'],
                IndexName='username-index',
                KeyConditionExpression='username = :current_user',
                ExpressionAttributeValues={
                    ':current_user': {'S': current_user}
                }
            )

            if 'Items' in invited:
                for item in invited.get("Items"):
                    invited_fires.append(
                        client_db.get_item(
                            TableName=os.environ['FIRES_TABLE'],
                            Key={
                                'fireId': {'S': item["fireId"]["S"]}
                            }
                        )
                    )

        return generate_response(200, {
            "success": True,
            "public": public_fires,
            "invited": invited_fires,
        })

    except Exception as e:
        return handle_exception(e)
