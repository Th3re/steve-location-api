import logging
from http import HTTPStatus

import api.app
from api.api.api import APICode
from api.channel.channel import LocationMessage, Location, ChannelResponse

LOG = logging.getLogger(__name__)


def post(location_request):
    LOG.debug(location_request)
    response = api.app.channel.send(LocationMessage(
        location=Location(
            latitude=location_request["latitude"],
            longitude=location_request["longitude"]
        ),
        user_id=location_request["userId"]
    ))
    if response.status == ChannelResponse.Status.ERROR:
        return {
            "code": APICode.ERROR,
            "message": "Cannot upload location",
            "userId": "108032329945935107776"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {
         "code": APICode.OK,
         "message": "Location uploaded",
         "userId": "108032329945935107776"
    }, HTTPStatus.OK
