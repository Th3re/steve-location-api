import abc
import enum
import json


class Message(abc.ABC):
    @abc.abstractmethod
    def serialize(self):
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, raw):
        pass


class ChannelResponse:
    class Status(enum.Enum):
        OK = "OK"
        ERROR = "ERROR"

    def __init__(self, message: str, status: Status):
        self.message = message
        self.status = status


class Channel(abc.ABC):
    @abc.abstractmethod
    def send(self, topic, data) -> ChannelResponse:
        pass


class LocationMessage(Message):
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude

    def serialize(self):
        return json.dumps(dict(dict(
            longitude=self.longitude,
            latitude=self.latitude,
        )))

    @classmethod
    def deserialize(cls, raw):
        data = json.loads(raw)
        return LocationMessage(latitude=data['latitude'], longitude=data['longitude'])
