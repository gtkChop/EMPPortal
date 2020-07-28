from emappcore.tools import BaseAppCorePluginInterface, BaseAppRoutePluginInterface
import logging

log = logging.getLogger(__name__)


class EMAppProjectManagementRegister(BaseAppCorePluginInterface, BaseAppRoutePluginInterface):
    """
    This is the project_mgmt registration process. Its is inherited from the Abstract class

    Inherited from abstract class BaseAppCorePluginInterface
    Inherited from abstract class BaseAppRoutePluginInterface

    Methods:

        app_api_actions: Register api functions and its method
        app_utilities: Register utility functions
        app_validators: Register validators. Registered validators are also available in schema
        app_schema: Register application schema

    """

    def app_api_actions(self, api):
        """
        Register api functions to the application. The apis are available at
        emappcore.tools import api_action

        Note: This will overwrite any existing API

        api.register will take 3 parameters
            - name: API name (str)
            - func: API function (function)
            - method: API method (GET, PUT, POST, DELETE)

        :param api: EMAppAPIActions class
        :return: None
        """

        return None

    def app_utilities(self, utility):
        """
        Register utility functions to the application. The utilities are available at
        emappcore.common import utilities

        utility.register will take 2 parameters
            - name: Utility name (str)
            - func: Utility function (function)

        Note: This will overwrite any existing utility function

        :param utility: is a class EMAppUtilities contains register method
        :return: None
        """

        _utilities = {

        }

        for name in _utilities:
            utility.register(
                name=name,
                func=_utilities[name]
            )

        return None

    def app_validators(self, validator):
        """
        Register all validators to the application. The validators are available at
        emappcore.common import validators

        Register validators are also available on any schemas file defined.
        e.g. Check user_schema.json

        validator.register will take 2 parameters
            - name: Validator name (str)
            - func: Validator function (function)

        Note: This will overwrite any existing validator function

        :param validator: class (EMAppValidators class)
        :return: None
        """

        return None

    def app_schema(self, schema):
        """
        Register app schemas here. schema can be accessed from emappcore.common import schemas.

        schema.register will take 3 parameters
            - schema_dir: Schema directory on which schema file available (str) - module type import
            - file_name: Schema file name. should be json
            - schema_name: Schema name (str) used to access schema content

        Note: This will overwrite any existing schema with same name

        :param schema: class (EMAppSchemas) contains register method
        :return: None
        """

        schema_dir = "emappext.project_mgmt.schema"

        _core_schemas = {
            "department_schema": "department_schema.json",
            "project_schema": "project_schema.json"
        }

        for schema_name in _core_schemas:
            schema.register(
                schema_dir=schema_dir,
                file_name=_core_schemas[schema_name],
                schema_name=schema_name
            )

        return None

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

