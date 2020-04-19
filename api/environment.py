import logging

from api.libs.environment.environmentreader import EnvironmentReader
from api.libs.representation.pretty import PrettyPrint

LOG = logging.getLogger(__name__)


class Channel(EnvironmentReader):
    def __init__(self):
        super()
        self.exchange = self.get('exchange')
        self.topic = self.get('topic')


class Rabbit(EnvironmentReader):
    def __init__(self):
        super()
        self.host = self.get('host')
        self.port = self.get('port')
        self.connection_attempts = int(self.get('connection_attempts'))
        self.retry_delay = int(self.get('retry_delay'))


class Server(EnvironmentReader):
    def __init__(self):
        super()
        self.port = self.get('port')


class Environment(PrettyPrint):
    def __init__(self):
        self.server = Server()
        self.rabbit = Rabbit()
        self.channel = Channel()

    @staticmethod
    def read():
        env = Environment()
        LOG.info(f'Environment: {env}')
        return env
