from django.views.generic.base import RedirectView
from django.urls import path, re_path
from collections import OrderedDict
from emappcore.utils import errors as err
import logging

log = logging.getLogger(__name__)


class EMAppRedirects:
    """
    This is the class contains all the redirects from different extensions/plugins.
    Existing redirects will be overwritten if any.

    Attributes:
        _redirects: dict holds all collected redirects

    Methods:
        register: register url redirects. This will be available in BaseAppRoutePluginInterface.redirects()
    """
    _redirects = OrderedDict()

    @classmethod
    def register(cls, from_url=None, to_url=None, dispatcher_type=None):
        """
        Register url redirects given from and to url

        :param from_url: str should be string
        :param to_url: str should be string
        :param dispatcher_type: Supported dispatcher_type is re_path and path
        :return: None
        """
        if from_url in cls._redirects:
            log.info("Overwriting the existing url redirect from_url: {} to {}".format(from_url, to_url))

        if dispatcher_type not in ("path", 're_path'):
            raise err.AppPluginError({
                "redirects": "error in dispatcher_type",
                "msg": "Supported types are path or re_path"
            })

        log.info("Adding redirects to tools from url: {} to url: {}".format(from_url, to_url))
        EMAppRedirects._redirects[from_url] = {
            "to_url": to_url,
            "type": dispatcher_type
        }

    @classmethod
    def get_redirects_to_url_dispatcher(cls):
        """
        This is for internal user only. Final collected url redirects are added to django url dispatcher.

        Internal user only

        :return: list
        """
        log.info("Fetching all redirects")
        _final_redirects = []
        for from_url in EMAppRedirects._redirects:
            _rd = cls._redirects[from_url]
            if _rd['type'] == "path":
                _final_redirects.append(
                    path(from_url, RedirectView.as_view(url=_rd['to_url']))
                )
            elif _rd['type'] == "re_path":
                _final_redirects.append(
                    re_path(from_url, RedirectView.as_view(url=_rd['to_url']))
                )
            else:
                raise err.UnexpectedError("Something wrond with the code logic")

        return _final_redirects


class EMAppRoutes:
    """
    This is the class contains all the routes from different extensions/plugins.
    Existing routes will be overridden by extension depending on the url_key in register.

    Attributes:
        _routes: dict holds all collected routes

    Methods:
        register: register url redirects. This will be available in BaseAppRoutePluginInterface.redirects()
    """
    _routes = OrderedDict()

    @classmethod
    def register(cls, url_key=None, django_urlconf_value=None):
        """
        This will be completely open and same as django url dispatcher. However,
        every url should have a url_key (friendly name). This url_key is used used to
        override any existing url/views in any extension.

        Django allows duplicate url patterns and always takes the first match. Hence url_key is used to take the latest
        duplicate url allowing us to modify any url

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


        :param url_key: str friendly name to each url
        :param django_urlconf_value: Same as django urlpatterns
        :return: None
        """
        if not url_key:
            raise err.AppPluginError("No url_key is given in register.py app_routes")

        if url_key in cls._routes:
            log.info("Overwriting the existing url route for url_key: {}".format(url_key))
        else:
            log.info("Adding route to tools from url_key: {}".format(url_key))
        EMAppRoutes._routes[url_key] = django_urlconf_value

    @classmethod
    def get_routes_to_url_dispatcher(cls):
        """
        This is for internal user only. Final collected url routes are added to django url dispatcher.

        Internal user only

        :return: list
        """
        log.info("Fetching all url routes")
        _final_routes = []
        for url_key in cls._routes:
            _final_routes.append(cls._routes[url_key])
        return _final_routes
