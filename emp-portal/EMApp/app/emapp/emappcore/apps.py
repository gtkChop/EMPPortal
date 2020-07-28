from django.apps import AppConfig
from emappcore.tools import register_extensions


class EMAppCoreConfig(AppConfig):
    """
    Core Employee Task Management Config process.

    Attributes:
        name: name of the plugin
        verbose_name: Label
    Methods:
        ready: This is where app collects information from all the installed apps/plugins
    """
    name = 'emappcore'
    verbose_name = "Core App module to register plugins"
    label = 'emappcore'

    def ready(self):
        """
        Start up script to collect all the information from the plugins before loading
        :return: None
        """
        core_app = register_extensions.AppRegister()
        core_app.setup()
        return None
