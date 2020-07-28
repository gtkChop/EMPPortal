from emappcore.tools import BaseAppCorePluginInterface, BaseAppRoutePluginInterface
from emappcore.utils import validators as core_validators, utilities as u
from emappcore.views.api_views import EMAppAPIView
from emappcore.views.authentication_views import EMAppLoginView, EMAppLogoutView, \
    EMAppPasswordResetView, EMAppPasswordResetDoneView, EMAppPasswordResetConfirmView, \
    EMAppPasswordResetCompleteView, EMAppPasswordChangeView
from emappcore.common import config
from django.urls import path, include
from django.contrib import admin
import logging
log = logging.getLogger(__name__)


class EMAppCorePluginRegister(BaseAppCorePluginInterface, BaseAppRoutePluginInterface):
    """
    This is the emappcore registration process. Its is inherited from the Abstract class

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
            "core_convert_to_bool": u.convert_to_bool,
            "get_application_title": u.get_application_title,
            "get_application_short_title": u.get_application_short_title,
            "get_application_terms_of_use_line1": u.get_application_terms_of_use_line1,
            "get_application_terms_of_use_copyrights": u.get_application_terms_of_use_copyrights,
            "generate_random_color_code": u.generate_random_color_code,
            "get_country_name": u.get_country_name,
            "prepare_relative_url_query_string": u.prepare_relative_url_query_string,
            "get_all_countries_select_option": u.get_all_countries_select_option,
            "prepare_error_data": u.prepare_error_data,
            "convert_request_data_to_dict": u.convert_request_data_to_dict,
            "list_slice": u.list_slice,
            "is_active_url": u.is_active_url
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
        _validators_dict = {
            "ignore_missing": core_validators.ignore_missing,
            "email_validator": core_validators.email_validator,
            "date_validator": core_validators.date_validator,
            "not_empty": core_validators.not_empty,
            "number_validator": core_validators.number_validator,
            "country_code_validator": core_validators.country_code_validator,
            "url_validator": core_validators.url_validator
        }
        for name in _validators_dict:
            validator.register(
                name=name,
                func=_validators_dict[name]
            )

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

        # Route for api
        log.info("Registering api route")
        route.register(
            url_key="app_api",
            django_urlconf_value=path(
                '{}<action_name>'.format(config.get('APPLICATION_API_ENDPOINT')),
                EMAppAPIView.as_view(),
                name='app_api'
            )
        )

        route.register(
            url_key="admin",
            django_urlconf_value=path('admin/', admin.site.urls)
        )

        # Register Login page
        route.register(
            url_key="login",
            django_urlconf_value=path('login/', EMAppLoginView.as_view(), name="login")
        )

        # Register Logout
        route.register(
            url_key="logout",
            django_urlconf_value=path('logout/', EMAppLogoutView.as_view(
                extra_context={
                    'next': "/login/"
                }
            ), name="logout")
        )

        # Change password
        route.register(
            url_key="change_password",
            django_urlconf_value=path('change-password/', EMAppPasswordChangeView.as_view(
                success_url='/logout'
                ),
                name='change_password'
            )
        )

        # Reset Password
        route.register(
            url_key="password_reset",
            django_urlconf_value=path('password-reset/', EMAppPasswordResetView.as_view(
                subject_template_name='registration/password_reset_subject.txt',
                email_template_name='registration/password_reset_email.html'
            ),
                                      name='password_reset')
        )

        # Reset password done
        route.register(
            url_key="password_reset_done",
            django_urlconf_value=path('password-reset/done/', EMAppPasswordResetDoneView.as_view(),
                                      name='password_reset_done')
        )

        # Confirm reset password url that will be sent to an email
        route.register(
            url_key="password_reset_confirm",
            django_urlconf_value=path('password-reset-confirm/<uidb64>/<token>/',
                                      EMAppPasswordResetConfirmView.as_view(),
                                      name='password_reset_confirm')
        )

        # Password reset complete
        route.register(
            url_key="password_reset_complete",
            django_urlconf_value=path('password-reset-complete/',
                                      EMAppPasswordResetCompleteView.as_view(),
                                      name='password_reset_complete')
        )

        return None

