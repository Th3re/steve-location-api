from api.channel.channel import Channel, LocationMessage, ChannelResponse


class RabbitChannel(Channel):
    def __init__(self):
        pass

    def send(self, message: LocationMessage) -> ChannelResponse:
        pass