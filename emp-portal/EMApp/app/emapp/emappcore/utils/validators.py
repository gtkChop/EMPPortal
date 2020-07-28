from emappcore.utils import errors as err
from email_validator import validate_email, EmailNotValidError
import pycountry
import validators as py_validators
from datetime import datetime
import logging

log = logging.getLogger(__name__)


def email_validator(key, value):
    """
    Verify if the given email id is valid or not. Raises a validation error if not valid.

    :param key: key value where the value is from
    :param value: value should be of type email
    :return: None
    """
    try:
        validate_email(value)
    except EmailNotValidError as e:
        raise err.ValidationError({
            key: "Not a valid email. Please verify your email"
        })


def date_validator(key, value):
    """
    Verify the given date string. The date string should be of format %Y-%m-%d (ISO).
    Note: string should be only of date type. Cannot accept datetime string.

    Raises error if does not match the format.

    :param key: key value where the value is from
    :param value: value shoudl be of type date string
    :return: None
    """

    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise err.ValidationError({
            key: "Given date string does not match the format %Y-%m-%d. Should be ISO format"
        })


def not_empty(key, value):
    """
    Verify if the value is empty or not. Raises validation error if empty
    Raises error if no value

    :param key: key value where the value is from
    :param value: value
    :return: None
    """
    if not value:
        raise err.ValidationError({
            key: "Value cannot be empty"
        })

    if isinstance(value, str) and not value.strip():
        raise err.ValidationError({
            key: "Value cannot be empty"
        })


def number_validator(key, value):
    """
    Check if the given value is number
    :param key: str
    :param value: str
    :return: None
    """
    try:
        int(value)
    except Exception as e:
        raise err.ValidationError({
            key: "Value must be integer"
        })


def ignore_missing(key, value):
    """
    Dummy functions
    :param key: key value where the value is from
    :param value: value
    :return: None
    """
    pass


def country_code_validator(key, value):
    """
    Validate the given country code. Country code should follow (ISO 3166) standards
    :param key: str
    :param value: str
    :return: None
    """
    try:
        _country = pycountry.countries.get(alpha_2=value)
        if not _country:
            raise err.ValidationError({
                key: "Not a valid country code - should follow ISO 3166 standard."
            })
    except Exception as e:
        log.error(e)
        raise err.ValidationError({
            key: "Something wrong with given country code - should follow ISO 3166 standard."
        })


def url_validator(key, value):
    """

    :param key:
    :param value:
    :return:
    """
    try:
        _val = py_validators.url(value)
        if not _val:
            raise Exception
    except Exception as e:
        raise err.ValidationError({
            key: "Not a valid url - use full url"
        })
