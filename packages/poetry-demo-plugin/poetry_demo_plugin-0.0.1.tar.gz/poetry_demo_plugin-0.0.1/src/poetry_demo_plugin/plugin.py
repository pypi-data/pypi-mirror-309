import logging
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry_demo_plugin.custom_command import CustomCommand



logger = logging.getLogger(__name__)


def factory():
    return CustomCommand()


class MyApplicationPlugin(ApplicationPlugin):
    def __init__(self) -> None:
        logger.debug("------- MyApplicationPlugin init ...")
        super().__init__()

    def activate(self, application):
        logger.debug("------- MyApplicationPlugin activate ...")
        application.command_loader.register_factory(
            "my-command", factory
        )

