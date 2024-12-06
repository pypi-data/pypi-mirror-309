from poetry.plugins.application_plugin import ApplicationPlugin

from openfund_plugin_up.command import OpenfundCommand


def factory():
    return OpenfundCommand()


class UpApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("openfund", factory)
