import connexion
from swagger_ui_bundle import swagger_ui_3_path

from api.channel.rabbit import create_connection, create_rabbit_channel
from api.environment import read_environment

OPENAPI_SPEC_DIR = "openapi/"
API_SPEC = "api.yaml"

env = read_environment()

rabbit_connection = create_connection(
    env.rabbit.host,
    env.rabbit.port,
    env.rabbit.connection_attempts,
    env.rabbit.retry_delay
)
channel = create_rabbit_channel(rabbit_connection, env.channel.exchange, env.channel.topic)


def main():
    options = {"swagger_path": swagger_ui_3_path}
    app = connexion.FlaskApp(
        __name__, specification_dir=OPENAPI_SPEC_DIR, options=options
    )
    app.add_api(
        API_SPEC,
        arguments={"title": "Location API"},
        resolver=connexion.resolver.RestyResolver("api.api"),
    )
    app.run(port=env.port)
