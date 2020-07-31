import requests
from emappcore.utils import errors as core_err
from emappcore.common import schemas
from emappext.hr_mgmt.utils import errors as hr_error
from emappext.hr_mgmt.tests import test_data
from emappext.hr_mgmt.models import Employee
from django.test import Client
from django.db import IntegrityError

url = "http://127.0.0.1/emapp/api/{}"


def send_api_post(api_headers=None, api_url=None, data=None):
    """
    Send api post requests with the given header, url and data.
    If any error raises a suitable error from the json response.
    :param api_headers:
    :param api_url:
    :param data:
    :return:
    """
    client = Client(**api_headers)
    _content_type = api_headers.get('content_type', '')
    if data:
        if _content_type:
            response = client.post(api_url, data, content_type=_content_type)
        else:
            response = client.post(api_url, data)
    else:
        response = requests.post(api_url)
    if response.status_code != 200:
        _response_data = response.json()
        _error_type = _response_data['error_type']
        _msg = _response_data['msg']
        if hasattr(core_err, _error_type):
            raise getattr(core_err, _error_type)(_msg)
        elif hasattr(hr_error, _error_type):
            raise getattr(hr_error, _error_type)(_msg)
        elif _error_type == "IntegrityError":
            raise IntegrityError(_msg)
        else:
            print(_response_data)
            raise Exception(_msg)

    return response.json(), response.status_code


def create_superuser():
    """
    Create super user and return api key
    :return:
    """
    superuser_data = {
        "date_of_birth": "1992-07-09",
        "first_name": "Swaroop",
        "last_name": "Bhat",
        "work_email": "swaroopbhatk@gmail.com",
        "nationality_code": "in",
        "employee_id": "DLX-EMP0",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "joining_date": "2018-10-01",
        "position": "Developer",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "role": "admin",
        "graduation_level": "bachelor",
        "contact_ph": "0899518706",
        "password": "test123456",
        "username": "gtkchop"
    }

    Employee.objects.create_superuser(**superuser_data)
    api_key, key = Employee.generate_api_key(superuser_data['work_email'])
    return api_key, key


def get_api_key(user_type=None, email=None):
    """
    Generate an api for the hr, admin and member
    :param user_type: str
    :return: str
    """
    if email:
        return Employee.generate_api_key(email)
    if user_type == "admin":
        return Employee.generate_api_key(test_data.employee_admin['work_email'])
    elif user_type == "hr":
        return Employee.generate_api_key(test_data.employee_hr['work_email'])
    elif user_type == "member":
        return Employee.generate_api_key(test_data.employee_member['work_email'])
    else:
        raise ValueError("User type not available")


def create_test_admin(headers=None):
    """
    Create a test admin user
    :return:
    """
    admin_data = test_data.employee_admin

    return send_api_post(api_headers=headers, api_url=url.format("create_employee"), data=admin_data)


def create_test_hr(headers):
    """
    Create a test hr user
    :return:
    """

    hr_data = test_data.employee_hr

    return send_api_post(api_headers=headers, api_url=url.format("create_employee"), data=hr_data)


def create_test_member(headers):
    """
    Create a test hr user
    :return:
    """

    member_data = test_data.employee_member

    return send_api_post(api_headers=headers, api_url=url.format("create_employee"), data=member_data)


def create_employee(headers, data):
    """
    Create any type of employee given headers and data
    :param headers: dict
    :param data: dict
    :return:
    """

    return send_api_post(api_headers=headers, api_url=url.format("create_employee"), data=data)


def update_employee(headers, data):
    """
    Update employee
    :param headers:
    :param data:
    :return:
    """
    return send_api_post(api_headers=headers, api_url=url.format("update_employee"), data=data)


def delete_employee(headers, data):
    """
    Delete employee
    :param headers:
    :param data:
    :return:
    """
    return send_api_post(api_headers=headers, api_url=url.format("delete_employee"), data=data)


def create_all_users(api_key):
    """
    create all types of users
    :return: None
    """
    api_headers = {
        "HTTP_API_KEY": api_key,
        'content_type': 'application/json; charset=UTF-8',
        'Accept': 'application/json'
    }
    create_test_admin(api_headers)
    create_test_hr(api_headers)
    create_test_member(api_headers)
    return None


def show_employee(api_headers, data, api_url=None):
    """

    :return:
    """
    api_url = url.format("show_employee")
    client = Client(**api_headers)
    _content_type = api_headers.get('content_type', '')
    if data:
        if _content_type:
            response = client.get(api_url, data, **api_headers)
        else:
            response = client.get(api_url, data)
    else:
        response = requests.get(api_url)
    if response.status_code != 200:
        _response_data = response.json()
        _error_type = _response_data['error_type']
        _msg = _response_data['msg']
        if hasattr(core_err, _error_type):
            raise getattr(core_err, _error_type)(_msg)
        elif hasattr(hr_error, _error_type):
            raise getattr(hr_error, _error_type)(_msg)
        else:
            raise Exception(_response_data)

    return response.json(), response.status_code


def get_schema_keys_given_role(action, role, schema_name="employee_schema"):
    """
    Get schema keys for a given role type. and action (show/update)
    :param schema_name: str
    :param action: str
    :param role: str
    :return: set
    """
    result = []
    properties = schemas.get_schema(schema_name)['properties']
    for _property, value in properties.items():
        if role in value[action]:
            result.append(_property)
    return set(result)


def delete_keys_from_employee_show(data_dict, del_keys):
    """
    Keys like id, created_at, updated_at are deleted to validate schema vs employee_show
    :param data_dict: dict
    :param del_keys: tuple
    :return: None
    """
    for _key in del_keys:
        del data_dict[_key]
    return data_dict
