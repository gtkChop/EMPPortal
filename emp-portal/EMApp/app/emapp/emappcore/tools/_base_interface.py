from emappcore.tools._api import EMAppAPIActions
from emappcore.tools._routes import EMAppRedirects, EMAppRoutes
from emappcore.common._essentials import EMAppUtilities, EMAppValidators, EMAppSchemas
import logging
log = logging.getLogger(__name__)


class BaseAppCorePluginInterface:
    """
    Abstract class for Core plugin. Responsible in registering API, utilities, validators and schemas.

    This should be inherited in the respective plugins in register.py and
    tools will extract all registered function during startup of the application.

    Methods:

        app_api_actions: To register api functions (GET, POST, PUT and DELETE)
        app_utilities: Register utilities/helpers of any app extensions here.
        app_validators: Register validators of any app extensions here.
        app_schema: Register application data schema/data model here.

    """

    def __init__(self):
        pass

    def app_api_actions(self, api):
        """
        Register api functions here using api.register(). Supports method (GET, PUT, POST and DELETE).

        api.register will take 3 parameters

            - name: API name (str)
            - func: API function (function)
            - method: API method (GET, PUT, POST, DELETE)

        :param api: class (EMAppAPIActions)
        :return: None
        """
        return None

    def app_utilities(self, utility):
        """
        Register utility functions to the application using utility.register().

        utility.register will take 2 parameters
            - name: Utility name (str)
            - func: Utility function (function)

        :param utility: class (EMAppUtilities)
        :return: None
        """
        return None

    def app_validators(self, validator):
        """
        Register all validators to the application using validator.register().
        Register validators are also available on any schemas file defined.

        validator.register will take 2 parameters
            - name: Validator name (str)
            - func: Validator function (function)

        :param validator: class (EMAppValidators class)
        :return: None
        """
        return None

    def app_schema(self, schema):
        """
        Register app schemas here using schema.register()

        schema.register will take 3 parameters
            - schema_dir: Schema directory on which schema file available (str) - module type import
            - file_name: Schema file name. should be json
            - schema_name: Schema name (str) used to access schema content

        :param schema: class (EMAppSchemas)
        :return: None
        """
        return None

    def register_core_interface(self):
        """
        New registration process other than core (_register_core_interface) should be added here.

        :return: None
        """
        return None

    def _register_core_interface(self):
        """
        This is the core registration process utilised by the tools to extract all required information.
        Do not modify this.

        To add any further registration, please use register_core_interface in respective plugin.

        :return: None
        """
        log.info("Registering core interface")
        log.info("Registering the app schema")
        self.app_schema(EMAppSchemas)
        log.info("Registering api functions to tools")
        self.app_api_actions(EMAppAPIActions)
        log.info("Registering validators to tools")
        self.app_validators(EMAppValidators)
        log.info("Registering utilities to tools")
        self.app_utilities(EMAppUtilities)

        self.register_core_interface()


class BaseAppRoutePluginInterface:
    """
    Abstract class for Core Route plugin. Same functionality as django url dispatcher.

    This should be inherited in the respective plugins in register.py and
    tools will extract all registered urls during startup of the application.

    Note: This will overwrite any existing routes/redirects, hence allows to modify functionality in any extension.

    Methods:

        redirects: Url redirects are registered here.
        route: All application routes and its views should be registered here.

    """

    def __init__(self):
        pass

    def app_redirects(self, redirect):
        """
        Register app redirects using redirect.register()

        redirect.register will take 3 parameters
            - from_url: From url type string. Note append string with r'<value>'
            - to_url: To url type string. Note append string with r'<value>'
            - dispatcher_type: django dispatcher type currently support path and re_path

        :param redirect: class (EMAppRedirects)
        :return: None
        """
        return None

    def app_route(self, route):
        """
        Register app redirects using route.register()

        This will be completely open and same as django url dispatcher. However,
        every url should have a url_key (friendly name). This url_key is used used to
        override any existing url/views in any extension.

        Django allows duplicate url patterns and always takes the first match. Hence url_key is used to take the latest
        duplicate url allowing us to modify any url

        So route.register() has 2 arguments
            - url_key: str (friendly name to each url)
            - django_urlcof_value: Same as django urlpatterns

        e.g.:

        route.register(
            url_key=about_blog_id,
            django_urlconf_value=path('about/', views.about, {'blog_id': 3})
        )

         route.register(
            url_key=author-polls,
            django_urlconf_value=path('author-polls/', include('polls.urls', namespace='author-polls'))
        )

        So if you give url_key=author_polls in some other extention all author-polls view function are replace with new
        views.


        :param route: class (EMPAppRoutes)
        :return: None
        """
        return None

    def register_route_interface(self):
        """
        New registration process other than core (_register_core_interface) should be added here.

        :return: None
        """
        return None

    def _register_route_interface(self):
        """
        This is the core registration process utilised by the tools to extract all required information.
        Do not modify this. Internal use only

        To add any further registration, please use register_route_interface in respective plugin register.py file.
        :return:
        """
        log.info("Adding redirects if any")
        self.app_redirects(EMAppRedirects)

        log.info("Adding all the urls and its corresponding views")
        self.app_route(EMAppRoutes)

        log.info("Adding any custom registration process if any")
        self.register_route_interface()


class BaseAppTemplateInterface:

    """
    TODO: Resolve template. Instead of using extends use app_extends
    Should inherit the existing template
    """
    def __init__(self):
        pass

    def _register_template_interface(self):
        """

        :return:
        """
        pass
