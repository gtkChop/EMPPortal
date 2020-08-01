from emappcore.utils import errors as err
from emappcore.common import config
from emappext.hr_mgmt import models
import os
import logging
log = logging.getLogger(__name__)


def validate_keys_employee_before_db(data_dict):
    """
    Validate keys. Some of the keys are internal. Hence do not allow those to modify
    :param data_dict: dict
    :return: None or raises an error
    """
    _not_allowed_keys = (
        '_api_key',
        'user',
        'employee',
        'id'
    )
    _intersection = tuple(set(data_dict.keys()).intersection(set(_not_allowed_keys)))
    if _intersection:
        raise err.ParameterNotAllowed({
            _intersection[0]: "The parameter not allowed"
        })


def validate_avatar_file(file_upload):
    """
    Validate the avatar uploaded or updated for an employee
    :param file_upload: class UploadedFile
    :return: Boolean
    """

    _allowed_formats = tuple(config.get('AVATAR_FILE_FORMATS', ["png", "jpeg", "jpg"]))

    file_name, file_ext = os.path.splitext(file_upload.name)
    if not file_ext or file_ext.replace(".", "").lower() not in _allowed_formats:
        raise err.ValidationError({
            "upload_avatar": "File not in required format only allowed format is png, jpeg and jpg"
        })

    if file_upload.size > int(config.get('MAX_AVATAR_SIZE_BYTES')):
        raise err.ValidationError({
            "avatar": "Uploaded image file exceeded limit."
        })

    return True


def validate_existing_user(key, value):
    """
    See if the user already exists. If exists raise an error existing user
    :return:
    """
    try:
        _employee = models.Employee.get_employee_by_id(value)
        raise err.ValidationError({
            key: "User with employee id already exists"
        })
    except err.NotFoundError:
        pass


def check_if_user_exists(key, value):
    """
    Check if the given employee exists
    :param key:
    :param value:
    :return:
    """
    try:
        _employee = models.Employee.get_employee_by_id(value)
    except err.NotFoundError:
        raise err.ValidationError(
            {
                key: "Given employee not found"
            }
        )