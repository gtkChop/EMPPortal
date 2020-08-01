from emappcore.common import schemas, model_transaction, validators, utilities as u
from emappcore.utils import model_helper, errors as err
from emappext.hr_mgmt import models
from emappext.hr_mgmt.index.employee_index import EmployeeDocument
from emappext.hr_mgmt.utils import auth, email
import os
import logging

log = logging.getLogger(__name__)


def create_employee(app_context, data_dict):
    """
    Used to create employee and user together. Two database tables that are to be populated is
    Employee and Profile. The given data is validated against json schema and custom validators.

    If any of the items in schema are not in the table column, those data goes to the extras table according
    to the group given in the schema. Allowed groups in employee schema are
    (profile, employee - these are the table names).

    Access:
        - Admin/Super User can add a new employee.
        - Only super user can add user as admin role
        - For all the other types of employee are added as member.

    Schema:
        Schema used to create employee: employee (see register.py).

    :param app_context: dict (contains user information)
    :param data_dict: dic
    :return: dict success message or show_employee - api
    """
    log.info("Checking authorization")
    auth.employee_create(app_context)
    _employee_id = data_dict.get('employee_id', '')
    _files = app_context.get('files', '')
    _show_employee = u.core_convert_to_bool(data_dict.pop('show_employee', True))

    if data_dict.get('skills', ''):
        _skills = data_dict['skills']
        if isinstance(_skills, str):
            # Hack for multipart/form-data?? Dont know if this is the right way
            # TODO: need to create a data insert pre processing pipeline
            data_dict['skills'] = [s.strip().title() for s in _skills.split(",")]

    log.info("Validating the given data for employee create")
    # Validate the data vs schema and model validate
    schemas.validate("employee_schema", data_dict)

    _properties = schemas.get_schema('employee_schema')['properties']

    log.info("Creating a employee for employee id: {}".format(_employee_id))
    try:
        with model_transaction.atomic():
            employee_model = models.Employee()
            employee_model.username = _employee_id
            _extras = []
            for _key in _properties:
                _val = data_dict.get(_key, '')

                if hasattr(employee_model, _key):
                    setattr(employee_model, _key, _val)
                else:
                    log.info("Adding to extras key - employee: {}".format(_key))
                    _extras.append(model_helper.create_extras_table_values(
                        extras_model=models.EmployeeExtras,
                        connecting_key="employee",
                        connecting_model=employee_model,
                        key=_key,
                        value=_val
                    ))

            if _files and _files.get('upload_avatar', ''):
                log.info("Found avatar create..")
                _uploaded_avatar = _files['upload_avatar']
                validators.validate_avatar_file(_uploaded_avatar)
                employee_model.avatar = _uploaded_avatar

            employee_model.save()
            for _md in _extras:
                _md.save()

    except Exception as e:
        log.error(e)
        raise e

    if _show_employee:
        result = show_employee(app_context, {"id": _employee_id})
    else:
        result = {
            "message": "Employee with id: {} has been created successfully".format(_employee_id)
        }

    email.send_email_create_employee(to=[data_dict.get('work_email').lower()])

    return result


def update_employee(app_context, data_dict):
    """
    Update employee profile. Parameter should contain id - representing unique id of the employee of id as employee id.
    Only admin/hr can alter employee fields or logged in user can alter their fields.

    Note:
        Access control is given in schema in update attribute - space separated string e.g. admin hr member all

        - admin: Only admin can update
        - admin hr: Only admin and to hr can update
        - admin hr member: admin , hr and member can update (logged in user ==  requested user profile)
        - all: show to every logged in user

    :param app_context: dict
    :param data_dict: dict (containing fields to be updated)
    :return: dict success message or show_employee - api
    """

    auth.is_authenticated(app_context)
    role = app_context.get('role')
    _show_employee = u.core_convert_to_bool(data_dict.pop('show_employee', True))
    _id = data_dict.pop('id', None)

    _files = app_context.get('files', '')
    _schema = schemas.get_schema('employee_schema')
    log.info("Updating an employee for an id: {}".format(_id))
    if data_dict.get('skills', ''):
        _skills = data_dict['skills']
        if isinstance(_skills, str):
            # Hack for multipart/form-data?? Dont know if this is the right way
            # TODO: need to create a data insert pre processing pipeline
            data_dict['skills'] = [s.strip().title() for s in _skills.split(",")]

    if role == "all":
        err.ValidationError({
            "InternalError": "This should not occur."
        })

    if not _id:
        raise err.ValidationError({
            "id": "id parameter is required."
        })

    try:
        with model_transaction.atomic():
            _employee = models.Employee.get_employee_by_id(_id)
            # Check authorization
            auth.employee_update({
                "role": app_context.get('role'),
                "user": app_context.get('user'),
                "employee": _employee
            })
            # Internal user only

            _data = _employee._as_dict()

            log.info("Updating the data and validating")
            _data.update(data_dict)
            schemas.validate("employee_schema", _data)

            # Insert operation
            _emp_extras = models.EmployeeExtras.objects.filter(employee=_employee)
            _extras = []

            for _key in data_dict:
                if _key in _schema['properties']:
                    try:
                        _property = _schema['properties'][_key]
                        _update = _property.get('update', "").split(" ")

                        if role not in _update:
                            raise err.NotAuthorizedError({
                                _key: "Not authorized to update the value"
                            })

                        if hasattr(_employee, _key):
                            setattr(_employee, _key, data_dict.get(_key))
                        else:
                            for _emp_ext in _emp_extras:
                                if _emp_ext.key == _key:
                                    _emp_ext.value = data_dict.get(_key)
                                    _extras.append(_emp_ext)
                                    break

                    except KeyError as e:
                        log.warning(e)
                        pass

            if 'upload_avatar' in _files:
                log.info("Found avatar update..")
                _uploaded_avatar = _files['upload_avatar']

                if _uploaded_avatar:
                    validators.validate_avatar_file(_uploaded_avatar)

                if _employee.avatar and os.path.isfile(_employee.avatar.path):
                    os.remove(_employee.avatar.path)
                _employee.avatar = _uploaded_avatar

            _employee.save()
            for _md in _extras:
                _md.save()

    except Exception as e:
        log.error(e)
        raise e

    if _show_employee:
        result = show_employee(app_context, {"id": _employee.employee_id})
    else:
        result = {
            "message": "Employee with id: {} has been updated successfully".format(_employee.employee_id)
        }

    return result


def show_employee(app_context, data_dict):
    """
    Show employee for the given employee id or employee unique identifier.

    Note: Access control is given is schema in show attribute - space separated string e.g. admin hr member all

        - admin: show to only to admin
        - admin hr: show admin and to hr
        - admin hr member: show admin and to hr and user profile (logged in user ==  requested user profile)
        - all: show to every logged in user

    :param app_context: dict
    :param data_dict: dict (containing employee_id oir id)
    :return: dict
    """
    log.info("Show employee api...")
    auth.employee_show(app_context)
    _user = app_context.get('user')
    role = app_context.get('role')
    _id = data_dict.get('id', '')
    _schema = schemas.get_schema('employee_schema')

    log.info("Showing the employee data for id: {}".format(_id))

    if not _id:
        raise err.ValidationError({
            "id": "id parameter is required."
        })

    _employee = models.Employee.get_employee_by_id(_id)

    # If logged in user and requesting profile are not same
    if role == "member":
        if _user.id != _employee.id:
            role = "all"

    _data = _employee.as_dict()

    response = dict()

    for _property in _schema['properties']:
        _show = _schema['properties'][_property].get('show', "").split(" ")
        if role in _show:
            response[_property] = _data[_property]

    for x in ("id", "created_at", "updated_at", "avatar"):
        response[x] = _data[x]

    return response


def _search_employee_for_pagination(app_context, data_dict):
    """
    This function is for internal use only. Utilized by views for pagination
    :return: Elastic search document
    """

    auth.is_authenticated(app_context)
    search_fields = data_dict.get('search_fields', '')
    search_value = data_dict.get('q', '')
    query_dict = data_dict.get('query_dict', '')

    if query_dict and not isinstance(query_dict, dict):
        raise err.ValidationError({
            "raw_query": "Raw query should be of type json"
        })

    if search_fields and not isinstance(search_fields, list):
        try:
            search_fields = search_fields.split(",")
            if not search_fields:
                raise err.ValidationError({
                    "search_fields": "Search fields should be list"
                })
        except Exception as e:
            log.error(e)
            raise err.ValidationError({
                "search_fields": "Something wrong while converting text to list in search_fields"
            })

    if not search_value and not query_dict:
        log.info("No search value given, returning all with limit")
        profiles = EmployeeDocument.search()
    else:
        if query_dict:
            log.info("given query dict for searching")
            profiles = EmployeeDocument.search().from_dict(query_dict)
        else:
            log.info("Given search value: {}".format(search_value))
            if not search_fields:
                search_fields = EmployeeDocument.default_search_fields_full_text()

            profiles = EmployeeDocument.search().query(
                'multi_match',
                query=search_value,
                fields=search_fields)

    return profiles


def search_employee(app_context, data_dict):
    """
    This api provides a way to search for an employee by
        - first name,
        - middle name
        - last name
        - work email
        - employee id
        - employee position
        - country

    Max limit is 100. If no search_fields are give - full text search is performed.
    Employee can also be searched from elastic search dictionary using parameter raw_query

    :parameter
        search_fields: list
            Fields to perform search operation, if not given defaulkt value is used
        search: str
            Value to be searched
        offset: int
            Offset
        limit: int
            max value is 100

    :param app_context: dict application context
    :param data_dict: dict
    :return: dict
    """
    limit = data_dict.get('limit', 20)
    offset = data_dict.get('offset', 0)
    if not isinstance(offset, int):
        raise err.ValidationError({
            'offset': "Offset should be integer"
        })

    if not isinstance(limit, int) or limit > 100:
        raise err.ValidationError({
            "limit": "Should be integer and max value allowed is 100"
        })

    # Authorization is checked in this function
    profiles = _search_employee_for_pagination(app_context, data_dict)

    results = {
        "results": [],
        "res_count": profiles.count()
    }

    for _p in profiles[offset:limit]:
        results['results'].append(_p.as_dict())
    return results


def delete_employee(app_context, data_dict):
    """
    Delete an employee given employee_id or unique id. Only admin or hr can delete employee.
    :param app_context:
    :param data_dict:
    :return:
    """
    auth.employee_delete(app_context)
    _id = data_dict.get('id', '')
    log.info("Deleting employee for an id: {}".format(id))

    if not _id:
        raise err.ValidationError({
            "id": "id parameter is required."
        })

    _employee = models.Employee.get_employee_by_id(_id)
    _employee.delete()

    return {
        "message": "Employee with id: {} has been deleted successfully".format(_id)
    }
