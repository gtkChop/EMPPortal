from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from emappcore.common import utilities
from jinja2.utils import escape


def template_utilities(request):
    """
    Application template context processor
    :param request: django request object
    :return: dict
    """
    logo_text = ""
    if request.user.is_authenticated:
        logo_text = request.user.first_name[0]+request.user.last_name[0]

    return {
        "u": utilities,
        "logo_text": logo_text.upper()
    }


def environment(**options):
    """
    This will be used by jinja2 templates. Django template engine
    doesnt allow function with parameters to be run on templates.
    Hence using jinja 2 which allows function to execute

    :param options:
    :return:
    """

    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse
    })
    env.filters.update({
        "empty_and_escape": empty_and_escape
    })
    return env


# Filters
def empty_and_escape(value):
    """
    returns '' for a None value else escapes the content useful for form
    elements.
    :param value:
    :return: ''
    """
    if value is None:
        return ''
    else:
        return escape(value)
