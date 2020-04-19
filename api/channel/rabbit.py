import logging

import pika.exceptions

from api.libs.channel.channel import Channel, ChannelResponse
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
        self.channel = None
        self.exchange = env.channel.exchange
        self.topic = env.channel.topic

    def _send_attempt(self, topic, data) -> ChannelResponse:
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.__exchange_type)
        routing_key = f'{self.topic}.{topic}'
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=data,
        )
        return ChannelResponse(
            message=f"Message uploaded to topic {topic}",
            status=ChannelResponse.Status.OK,
        )

    def send(self, topic, data) -> ChannelResponse:
        try:
            return self._send_attempt(topic, data)
        except Exception as amqp_error:
            LOG.error(f'Send attempt error: {amqp_error}')
            try:
                self.channel = create_connection(
                    self.env.rabbit.host,
                    self.env.rabbit.port,
                    self.env.rabbit.connection_attempts,
                    self.env.rabbit.retry_delay
                )
                return self._send_attempt(topic, data)
            except Exception as general_exception:
                LOG.error(f'Unexpected exception after reconnecting to rabbit: {general_exception}')
                return ChannelResponse(
                    message=f"Cannot publish message to {self.env.channel.topic}",
                    status=ChannelResponse.Status.ERROR,
                )
