import logging
from http import HTTPStatus

import api.app
from api.api.api import APICode
from api.channel.channel import LocationMessage, Location, ChannelResponse

LOG = logging.getLogger(__name__)


def post(location_request):
    LOG.debug(location_request)
    user_id = location_request['userId']
    response = api.app.channel.send(LocationMessage(
        location=Location(
            latitude=location_request["latitude"],
            longitude=location_request["longitude"]
        ),
        user_id=user_id
    ))
    if response.status == ChannelResponse.Status.ERROR:
        return {
            "code": APICode.ERROR,
            "message": "Cannot upload location",
            "userId": user_id
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {
         "code": APICode.OK,
         "message": "Location uploaded",
         "userId": user_id
    }, HTTPStatus.OK
