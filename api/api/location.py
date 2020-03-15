import logging
from http import HTTPStatus


LOG = logging.getLogger(__name__)


def post(location_request: dict) -> dict:
    LOG.debug(location_request)
    return {
         "code": "OK",
         "message": "Location uploaded",
         "userId": "108032329945935107776"
    }, HTTPStatus.OK
