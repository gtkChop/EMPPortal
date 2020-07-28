from emappcore.utils import errors as err
import logging

log = logging.getLogger(__name__)


def is_authenticated(app_context, raise_errors=True):
    """
    Check if the user is logged in or anonymous user. If raise error, raise not authorized error

    :param app_context: dict
    :param raise_errors: boolean
    :return: boolean or raise errors
    """
    log.info("Checking if the user is authenticated")
    user = app_context.get('user')
    if user.is_authenticated:
        return True
    else:
        if raise_errors:
            raise err.NotAuthorizedError({
                "user": "You are not logged in to perform this action"
            })
        else:
            return False


def employee_create(app_context, raise_errors=True):
    """
    Check if the logged in user has access to create an employee.
    if raise errors = True. This will raise NotAuthorized error else return boolean.

    Rules:
        - Admin/super user user can create employee
        - Admin/super user can create another admin
        - Admin cab create user.

    :param app_context: dict (contains user information)
    :param raise_errors: boolean (if true raises NotAuthorizedError)
    :return: boolean or raises error
    """
    log.info("Validating employee create access")
    _role = app_context.get('role', '')
    _is_super_user = app_context.get('is_superuser', False)

    if _is_super_user:
        return True

    if _role not in ('admin', 'hr'):
        if raise_errors:
            raise err.NotAuthorizedError({
                "user": "You are not authorised to create employee"
            })
        else:
            return False

    return True


def employee_update(app_context, raise_errors=True):
    """
    Check if the logged in user has access to update an employee.
    if raise errors = True. This will raise NotAuthorized error else return boolean.

    Rules:
        - Admin/super user user can update employee
        - Logged in user can update his own profile.
        - Any logged in user cannot update

    :param app_context: dict (contains user information)
    :param raise_errors: boolean (if true raises NotAuthorizedError)
    :return: boolean or raises error
    """
    log.info("Validating employee create access")
    _role = app_context.get('role', '')
    _is_super_user = app_context.get('is_superuser', False)

    if _is_super_user or _role in ('admin', 'hr'):
        return True

    # Anonymous cannot update user
    # Only admin/hr or logged in person can update his/her profile.
    if not _role or app_context.get('user').id != app_context.get('employee').id:
        if raise_errors:
            raise err.NotAuthorizedError({
                "user": "Not authorized to perform update action."
            })
        else:
            return False

    return True


def employee_show(app_context, raise_errors=True):
    """
    Check if the logged in user has access to get an employee.
    if raise errors = True. This will raise NotAuthorized error else return boolean.

    Rules:
        - Admin/super user can see all employee
        - Logged in user can see his own profile.
        - Any logged in user cannot see profile with limited information

    :param app_context: dict (contains user information)
    :param raise_errors: boolean (if true raises NotAuthorizedError)
    :return: boolean or raises error
    """
    log.info("Validating employee show access")
    _user = app_context.get('user')

    if _user.is_authenticated:
        return True
    else:
        if raise_errors:
            raise err.NotAuthorizedError({
                "user": "Not authorized to see profile."
            })
        else:
            return False


def employee_delete(app_context, raise_errors=True):
    """
    Check an authorization of the user for employee delete operations
    :param app_context: dict
    :param raise_errors: If true raise Notauthorized errors
    :return: Boolean
    """
    log.info("Validating employee delete access")
    role = app_context.get('role')
    if role not in ('admin', "hr"):
        if raise_errors:
            raise err.NotAuthorizedError({
                "user": "User not authorized to delete employee"
            })
        else:
            return False
    return True
