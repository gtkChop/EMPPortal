from emappcore.common import config
from emappcore.utils import utilities as u
from django.conf import settings
from django.apps import apps
import pkg_resources
import logging
log = logging.getLogger(__name__)


class AppRegister:
    """
    Register all installed custom extensions of plugins. Collect all necessary information from register.py
    register.py should contain class same as entry point given in setup.py and
    should be inherited from any of the base interface.

    Methods:
        setup: set up application
    """
    def __init__(self):
        """
        Attributes:
            config: app config from config.yaml file

        """
        self._config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def _get_app_config(self):
        """
        Extract configuration from settings file and load to confg dict.
        All config can be extracted from from core.commpon import config.

        Wrapper to core config

        :return: None
        """
        log.info("Registering configuration")
        for cnf in dir(settings):
            if not cnf.startswith("_") and cnf.isupper():
                config[cnf] = getattr(settings, cnf)

        self.config = config
        log.info("Configuration registered successfully")
        # Display App name
        u.display_app_name()

    def _registration_sequence(self, _extension):
        """
        Register a given extension in a sequence given extension
        :return: None
        """
        # Core helper, validator and api interface
        if hasattr(_extension, "_register_core_interface"):
            _extension._register_core_interface()

        # Core routes and redirects interface
        if hasattr(_extension, "_register_route_interface"):
            _extension._register_route_interface()

        # Core template interface
        if hasattr(_extension, "_register_template_interface"):
            _extension.__register_template_interface()

    def _register_extensions(self):
        """
        Get all the installed custom extension registered. Please note extensions must be installed
        and should have an entry point emapp.register. Otherwise extensions will be ignored.

        :return: None
        """
        log.info("Collecting all registered extensions")
        installed_apps = [app.label for app in apps.get_app_configs()]
        log.info("Found installed apps: ")
        log.info(installed_apps)

        for _entry_point in pkg_resources.iter_entry_points('emapp.register'):
            if _entry_point.name in installed_apps:
                log.info("Found custom entry point: {}".format(_entry_point.name))
                _extension = _entry_point.load()()
                self._registration_sequence(_extension)

    def setup(self):
        """
        Setup an application
        :return: None
        """
        self._get_app_config()
        self._register_extensions()


