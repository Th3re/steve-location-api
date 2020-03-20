import json
import logging

import pika.exceptions

from api.channel.channel import Channel, LocationMessage, ChannelResponse

LOG = logging.getLogger(__name__)


def create_connection(host, port, connection_attempts, retry_delay):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host, port=port, connection_attempts=connection_attempts, retry_delay=retry_delay))
    channel = connection.channel()
    return channel


def create_rabbit_channel(channel, exchange, topic):
    rabbit_channel = RabbitChannel(channel, exchange=exchange, topic=topic)
    return rabbit_channel


class RabbitChannel(Channel):
    __exchange_type = 'topic'

    def __init__(self, channel, exchange, topic):
        self.channel = channel
        self.exchange = exchange
        self.topic = topic

    @staticmethod
    def __serialize_message(message: LocationMessage):
        location = message.location
        body = json.dumps(dict(
            longitude=location.longitude,
            latitude=location.latitude,
        ))
        return body

    def send(self, message: LocationMessage) -> ChannelResponse:
        try:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__exchange_type)
        except pika.exceptions.AMQPError as amqp_error:
            LOG.error(amqp_error)
            return ChannelResponse(
                message=f"Cannot declare exchange {self.exchange} of type {self.__exchange_type}",
                status=ChannelResponse.Status.ERROR,
            )
        user_id = message.user_id
        routing_key = f'{self.topic}.{user_id}'
        body = self.__serialize_message(message)
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=body,
            )
        except pika.exceptions.AMQPError as amqp_error:
            LOG.error(amqp_error)
            return ChannelResponse(
                message=f"Cannot publish message to {routing_key}",
                status=ChannelResponse.Status.ERROR,
            )
        return ChannelResponse(
            message=f"Location uploaded for user {user_id}",
            status=ChannelResponse.Status.OK,
        )
