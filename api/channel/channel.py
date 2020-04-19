import json

from api.libs.channel.channel import Message


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
