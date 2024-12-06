from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.helpers import argument
from cleo.helpers import option

from poetry.console.commands.env_command import EnvCommand
from poetry.utils._compat import WINDOWS

from poetry_plugin_openfund.command import OpenfundCommand

from binance.spot import Spot as Client


if TYPE_CHECKING:
    from poetry.core.masonry.utils.module import Module


class OpenfundRunCommand(EnvCommand, OpenfundCommand):
    name = "openfund times"
    description = "Runs a command in the appropriate environment."

    arguments = [
        argument(
            "args", "The command and arguments/options to run.", multiple=True
        )
    ]
    options = [
        # option(
        #     "group",
        #     "-G",
        #     "The group to add the dependency to.",
        #     flag=False,
        # ),
    ]
    loggers = ["poetry_plugin_openfund"]

    def handle(self) -> int:
        client = Client()
        print(client.time())
        # args = self.argument("args")
        # script = args[0]
        # scripts = self.poetry.local_config.get("scripts")

        # if scripts and script in scripts:
        #     return self.run_script(scripts[script], args)

        # try:
        #     return self.env.execute(*args)
        # except FileNotFoundError:
        #     self.line_error(
        #         f"<error>Command not found: <c1>{script}</c1></error>"
        #     )
        #     return 1
        return 0
