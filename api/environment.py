import os

APP_PORT = "APP_PORT"


class Environment:
    def __init__(self, port="8080"):
        self.port = port


def read_environment() -> Environment:
    port = os.environ.get(APP_PORT, "8080")
    return Environment(port=port)
