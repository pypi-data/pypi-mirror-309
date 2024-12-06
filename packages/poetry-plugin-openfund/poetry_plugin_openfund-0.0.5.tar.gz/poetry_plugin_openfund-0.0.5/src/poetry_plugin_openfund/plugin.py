from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_plugin_openfund.command import OpenfundCommand


def factory():
    return OpenfundCommand()


class OpenfundApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("openfund", factory)
