from emappcore.common import config
from urllib.parse import urlparse
from pathlib import PurePosixPath
import pyfiglet
import random
import pycountry
import logging
log = logging.getLogger(__name__)


def display_app_name():
    """
    Display Application name during start up.
    :return: None
    """
    _app_title = config.get('APPLICATION_SHORT_TITLE').upper() or config.get('APPLICATION_TITLE').upper()
    _env = config.get('ENVIRONMENT').lower()
    result = pyfiglet.figlet_format(_app_title)
    print(result)
    print("Environment: {}".format(_env))
    print("\n")


def convert_to_bool(value):
    """
    Convert the given value to bool
    :return: boolean
    """

    if not value:
        return False

    if isinstance(value, str) or isinstance(value, int):
        value = str(value).lower()
        if value in ('true', "1"):
            return True

    return False


def get_application_title():
    """
    Get the application title from the config
    :return: str
    """
    return config.get("APPLICATION_TITLE", "Title not given")


def get_application_short_title():
    """
    Get application short title from config
    :return: str
    """
    return config.get('APPLICATION_SHORT_TITLE', "Short title not given")


def get_application_terms_of_use_line1():
    """
    Get application usage terms from config
    :return:
    """
    _company_name = config.get("COMPANY_NAME")
    return config.get('APPLICATION_TERMS_OS_USE_LINE1')+_company_name


def get_application_terms_of_use_copyrights():
    """
    Get application usage terms from config
    :return:
    """
    return config.get('APPLICATION_TERMS_OS_USE_COPYRIGHT')


def generate_random_color_code():
    """
    Generate random color code from the selected colors
    :return:
    """
    _colors = (
        "#e91e63",
        "#9c27b0",
        "#3f51b5",
        "#2196f3",
        "#03a9f4",
        "#00bcd4",
        "#795548",
        "#4caf50"
    )

    return random.choice(_colors)


def get_country_name(country_code):
    """
    Get country name given country code.
    :param country_code: str
    :return: str
    """

    if not country_code:
        return ""

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if not country:
            return ""
        return country.name
    except Exception as e:
        log.error(e)
        return ""


def get_all_countries_select_option():
    """

    :return:
    """
    options = [{"value": x.alpha_2, "text": x.name} for x in list(pycountry.countries)]

    return options


def prepare_relative_url_query_string(request, param_to_add):
    """
    TODO need optimization

    :param request:
    :param param_to_add:
    :return:
    """
    # TODO need optimization

    try:
        if request.GET:
            _u = urlparse(request.get_full_path())
            _q_dict = dict([x.split("=") for x in _u.query.split('&')])
            try:
                del _q_dict[param_to_add]
            except KeyError:
                pass
            query_string = "&".join(['{}={}'.format(_k, _v) for _k, _v in _q_dict.items()])
            if query_string:
                relative_path = request.path + '?' + query_string + '&'
            else:
                relative_path = request.path + "?"
        else:
            relative_path = request.path + '?'

        return relative_path
    except Exception as e:
        log.error(e)
        return request.get_full_path()


def prepare_error_data(error_dict):
    """
    Prepare error data according to the required format
    :param error_dict:
    :return:
    """
    if not error_dict:
        return error_dict

    if isinstance(error_dict, dict):
        for key in error_dict:
            error_dict[key] = [error_dict.get(key)]

    return error_dict


def convert_request_data_to_dict(requests_query_dict):
    """
    Convert django queryDict object to dict
    :param requests_query_dict:
    :return: dict
    """
    data_dict = dict()
    for key in requests_query_dict:
        _val = requests_query_dict.getlist(key)
        if len(_val) > 1:
            data_dict[key] = _val
        else:
            data_dict[key] = _val[0]
    return data_dict


def list_slice(ls, from_indx, to_index):
    """
    Slice the given list between from and to value
    :param ls: list
    :param from_indx: int
    :param to_index: int
    :return: list
    """
    return ls[from_indx:to_index]


def is_active_url(pattern, request):
    """
    Check if the url is active. i.e. if the given patter matches in request.path return active
    :param pattern: string
    :param request: request object
    :return: str
    """

    try:
        if request.path == pattern:
            return 'active'
    except Exception as e:
        log.warning(e)

    return ''

