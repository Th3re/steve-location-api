import connexion
import logging
from swagger_ui_bundle import swagger_ui_3_path

from api.channel.rabbit import create_connection, create_rabbit_channel
from api.environment import read_environment

OPENAPI_SPEC_DIR = "openapi/"
API_SPEC = "api.yaml"

logging.basicConfig(level=logging.DEBUG)
env = read_environment()

channel = create_rabbit_channel(env)


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
