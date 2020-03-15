import abc
import enum
from collections import namedtuple

Location = namedtuple("Location", ["latitude", "longitude"])


class LocationMessage:
    def __init__(self, location: Location, user_id: str):
        self.location = location
        self.user_id = user_id


class ChannelResponse:
    class Status(enum.Enum):
        OK = "OK"
        ERROR = "ERROR"

    def __init__(self, message: str, status: Status):
        self.message = message
        self.status = status


class Channel(abc.ABC):
    @abc.abstractmethod
    def send(self, message: LocationMessage) -> ChannelResponse:
        pass
