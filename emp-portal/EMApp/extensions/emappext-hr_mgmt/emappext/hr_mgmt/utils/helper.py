from emappcore.common import schemas
from emappext.hr_mgmt.models import Employee
from emappext.hr_mgmt.index.employee_index import EmployeeDocument
from emappext.hr_mgmt.utils import errors as err, auth
import logging

log = logging.getLogger(__name__)


def get_user_given_email(user_email):
    """
    Get the user for a given email id.
    :param user_email: str email
    :return: str
    """
    user = Employee.objects.get(work_email=user_email)
    if not user:
        raise err.UserNotFoundError({
            "email": "user not found for a given user email."
        })

    return user


def get_user_full_name(user_model):
    """
    Get the user first name given user model
    :return: str
    """
    if isinstance(user_model, dict):
        return "{last_name}, {first_name}".format(
            last_name=user_model.get('last_name').capitalize(),
            first_name=user_model.get('first_name').capitalize()
        )

    return "{last_name}, {first_name}".format(
        last_name=user_model.last_name.capitalize(),
        first_name=user_model.first_name.capitalize()
    )


def get_user_by_id(user_id):
    """
    Gte employee by id
    :param user_id:
    :return:
    """
    emp = Employee.get_employee_by_id(user_id)

    return emp


def get_schema_groups(schema_name):
    """
    Get schema grouop given schema group
    :param schema_name: str
    :return: tuple
    """
    _schema = schemas.get_schema(schema_name)
    groups = dict()
    for _property in _schema['properties']:
        _gp = _schema['properties'][_property].get('group_label', '')
        if _gp in groups:
            groups[_gp].append(_property)
        else:
            groups[_gp] = [_property]

    return groups


def employee_verify_access(action, logged_user, emp_id=None):
    """
    Verify access for the given action
    :param action:
    :param logged_user:
    :param emp_id:
    :return:
    """
    context = {
        "role": logged_user.role,
        "is_superuser": logged_user.is_superuser,
        "employee": Employee.get_employee_by_id(emp_id) if emp_id else None
    }

    return getattr(auth, action)(context, raise_errors=False)


def get_total_employee_count():
    """
    Get total active employee count
    :return:
    """
    return EmployeeDocument.search().count()


def convert_string_to_html_id(value):
    """
    Convert string to html id (remove scape and replace by -)
    :param value: str
    :return: str
    """
    if not value:
        return value

    value = value.lower().split(" ")
    return "-".join(value)


def convert_list_to_comma_separated_text(value, is_title=True):
    """
    convert text to comma separated text to display to ui
    :return:
    """
    if not value:
        return ""

    if is_title:
        _value = [x.strip().title() for x in value]
        return ",".join(_value)

    return ".".join(value)
