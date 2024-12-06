import logging
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_plugin_openfund.command import OpenfundCommand
from poetry_plugin_openfund.binance_tools.openfund_times import (
    OpenfundRunCommand,
)

logger = logging.getLogger(__name__)


def factory_OpenfundRunCommand():
    return OpenfundRunCommand()


def factory_OpenfundCommand():
    return OpenfundCommand()


class OpenfundApplicationPlugin(ApplicationPlugin):
    def __init__(self) -> None:
        logger.debug("------- OpenfundApplicationPlugin init ...")
        super().__init__()

    def activate(self, application):
        logger.debug("------- OpenfundApplicationPlugin activate ...")
        application.command_loader.register_factory(
            "openfund", factory_OpenfundCommand
        )
        application.command_loader.register_factory(
            "openfund tiems", factory_OpenfundRunCommand
        )
