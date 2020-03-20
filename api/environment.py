import os


class Channel:
    EXCHANGE = "CHANNEL_EXCHANGE"
    TOPIC = "CHANNEL_TOPIC"

    def __init__(self, exchange, topic):
        self.exchange = exchange
        self.topic = topic


class Rabbit:
    HOST = "RABBIT_HOST"
    PORT = "RABBIT_PORT"
    CONNECTION_ATTEMPTS = "RABBIT_CONNECTION_ATTEMPTS"
    RETRY_DELAY = "RABBIT_RETRY_DELAY"

    def __init__(self, host, port, connection_attempts, retry_delay):
        self.host = host
        self.port = port
        self.connection_attempts = connection_attempts
        self.retry_delay = retry_delay


class Environment:
    PORT = "PORT"

    def __init__(self, rabbit: Rabbit, channel: Channel, port="8080"):
        self.port = port
        self.rabbit = rabbit
        self.channel = channel


def read_environment() -> Environment:
    port = os.environ.get(Environment.PORT, "8080")
    return Environment(
        port=port,
        rabbit=Rabbit(
            host=os.environ.get(Rabbit.HOST),
            port=os.environ.get(Rabbit.PORT),
            connection_attempts=int(os.environ.get(Rabbit.CONNECTION_ATTEMPTS)),
            retry_delay=int(os.environ.get(Rabbit.RETRY_DELAY))
        ),
        channel=Channel(
            exchange=os.environ.get(Channel.EXCHANGE),
            topic=os.environ.get(Channel.TOPIC)
        )
    )
