import logging
from http import HTTPStatus

import api.app
from api.api.api import APICode
from api.channel.channel import LocationMessage, ChannelResponse

LOG = logging.getLogger(__name__)


def post(location_request):
    LOG.debug(location_request)
    user_id = location_request['userId']
    location_message = LocationMessage(
            latitude=location_request["latitude"],
            longitude=location_request["longitude"]
    )
    response = api.app.channel.send(topic=user_id, data=location_message.serialize())
    if response.status == ChannelResponse.Status.ERROR:
        LOG.error(response.message)
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
