import json
import logging

import pika.exceptions

from api.channel.channel import Channel, LocationMessage, ChannelResponse
from api.environment import Environment

LOG = logging.getLogger(__name__)


def create_connection(host, port, connection_attempts, retry_delay):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host, port=port, connection_attempts=connection_attempts, retry_delay=retry_delay))
    channel = connection.channel()
    return channel


def create_rabbit_channel(env: Environment):
    rabbit_channel = RabbitChannel(env)
    return rabbit_channel


class RabbitChannel(Channel):
    ATTEMPTS = 10
    __exchange_type = 'topic'

    def __init__(self, env: Environment):
        self.env = env
        self.channel = create_connection(
            env.rabbit.host,
            env.rabbit.port,
            env.rabbit.connection_attempts,
            env.rabbit.retry_delay
        )
        self.exchange = env.channel.exchange
        self.topic = env.channel.topic

    @staticmethod
    def __serialize_message(message: LocationMessage):
        location = message.location
        body = json.dumps(dict(
            longitude=location.longitude,
            latitude=location.latitude,
        ))
        return body

    def _send_attempt(self, message: LocationMessage) -> ChannelResponse:
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

    def send(self, message: LocationMessage) -> ChannelResponse:
        for _ in range(self.ATTEMPTS):
            try:
                return self._send_attempt(message)
            except ConnectionError:
                self.channel = self.channel = create_connection(
                    self.env.rabbit.host,
                    self.env.rabbit.port,
                    self.env.rabbit.connection_attempts,
                    self.env.rabbit.retry_delay
                )
