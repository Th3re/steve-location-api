import connexion
import logging
from swagger_ui_bundle import swagger_ui_3_path

from api.libs.channel.rabbit.channel import RabbitChannel
from api.environment import Environment


logging.basicConfig(level=logging.DEBUG)
env = Environment.read()


channel = RabbitChannel.create(env.channel, env.rabbit)


def main():
    options = {"swagger_path": swagger_ui_3_path}
    app = connexion.FlaskApp(
        __name__, specification_dir="openapi/", options=options
    )
    app.add_api(
        "api.yaml",
        arguments={"title": "Location API"},
        resolver=connexion.resolver.RestyResolver("api.api"),
    )
    app.run(port=env.server.port)
