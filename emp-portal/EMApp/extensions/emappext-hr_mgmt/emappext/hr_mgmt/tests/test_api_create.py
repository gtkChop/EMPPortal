from rest_framework.test import APITestCase
from emappcore.utils import errors as core_err
from emappext.hr_mgmt.tests import helper as h
from emappext.hr_mgmt.tests import create_data
from django.db import IntegrityError
from django.test import Client
import os
import copy
import logging

log = logging.getLogger(__name__)


class EmployeeCreateAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up all the required data here.
            - Setup admin user
            - Setup hr user
            - Setup member
        :return: None
        """

        api_key, cls._superuser_key = h.create_superuser()
        h.create_all_users(cls._superuser_key)
        api_key, cls._admin_key = h.get_api_key("admin")
        api_key, cls._hr_key = h.get_api_key("hr")
        api_key, cls._member_key = h.get_api_key("member")
        return None

    def setUp(self):
        pass

    def test_api_headers_wrong_key(self):
        """
        content type should be application json
        :return:
        """
        # Wrong headers
        with self.assertRaises(core_err.NotAuthorizedError):
            resp, code = h.create_test_member(
                {
                    "HTTP_API_KEY": "asdasd",
                    'Accept': 'application/json'
                }
            )

    def test_employee_create_api_without_auth(self):
        """
        Test employee create without api-key or wrong api-key
        :return: None
        """
        # Wrong api key
        with self.assertRaises(core_err.NotAuthorizedError):
            resp, code = h.create_test_member(
                {
                    "HTTP_API_KEY": "asdasd",
                    'content_type': 'application/json; charset=UTF-8',
                    'Accept': 'application/json'
                }
            )

        # No api key
        with self.assertRaises(core_err.NotAuthorizedError):
            resp, code = h.create_test_member(
                {
                    'content_type': 'application/json; charset=UTF-8',
                    'Accept': 'application/json'
                }
            )

    def test_employee_create_api_with_admin_auth(self):
        """
        Test employee create with admin rights. Should be successful
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        res, code = h.create_employee(api_headers, create_data.test_data_created_by_admin)
        self.assertEqual(code, 200)

    def test_employee_create_api_with_hr_auth(self):
        """
        Test employee create with hr rights. Should be successful
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)
        self.assertEqual(code, 200)

    def test_employee_create_api_with_member_auth(self):
        """
        Test employee create with hr rights. Should be successful
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.create_employee(api_headers, create_data.test_data_created_by_member)

    def test_employee_create_duplicate_record(self):
        """
        Test employee create with duplicate record
        :return:
        """
        # Should be successful - first data
        # Super user
        api_headers = {
            "HTTP_API_KEY": self._superuser_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)
        self.assertEqual(code, 200)

        # admin
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        with self.assertRaises(IntegrityError):
            res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)

        # hr
        api_headers = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        with self.assertRaises(IntegrityError):
            res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)

        # superuser
        api_headers = {
            "HTTP_API_KEY": self._superuser_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        with self.assertRaises(IntegrityError):
            res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)

    def test_employee_create_duplicate_employee_id(self):
        """
        Test employee with duplicate employee_id
        :return:
        """
        duplicate_emp_id = create_data.test_data_created_by_member['employee_id']
        # Should be successful - first data
        # Super user
        api_headers = {
            "HTTP_API_KEY": self._superuser_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # Create a first data as member
        res, code = h.create_employee(api_headers, create_data.test_data_created_by_member)
        self.assertEqual(code, 200)

        # admin
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # Hr data but same employee id
        _data = create_data.test_data_created_by_hr
        _data['employee_id'] = duplicate_emp_id
        with self.assertRaises(IntegrityError):
            res, code = h.create_employee(api_headers, _data)

    def test_employee_create_duplicate_work_email(self):
        """
       Test employee with duplicate work_email
       :return:
       """
        duplicate_work_email = create_data.test_data_created_by_admin['work_email']
        # Should be successful - first data
        # Super user
        api_headers = {
            "HTTP_API_KEY": self._superuser_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # Create a first data as member
        res, code = h.create_employee(api_headers, create_data.test_data_created_by_admin)
        self.assertEqual(code, 200)

        # admin
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # Hr data but same employee id
        _data = create_data.test_data_created_by_member
        _data['work_email'] = duplicate_work_email
        with self.assertRaises(IntegrityError):
            res, code = h.create_employee(api_headers, _data)

    def test_employee_create_by_member_auth(self):
        """
        Test employee create api with member api. Member should be allowed to create profile/employee
        :return:
        """
        # member
        api_headers = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # create hr
        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.create_employee(api_headers, create_data.test_data_created_by_hr)

    def test_employee_create_with_different_role(self):
        """
        Test employee with not not in admin/hr/member
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # create hr
        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            _data['role'] = "asdasdad"
            res, code = h.create_employee(api_headers, _data)

        # Missing role
        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            _data['role'] = ""
            res, code = h.create_employee(api_headers, _data)

    def test_employee_create_minimum_fields(self):
        """
        Test employee create with only mandatory fields
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # create hr
        res, code = h.create_employee(api_headers, create_data.test_data_minimum_fields)
        self.assertEqual(code, 200)

    def test_employee_create_without_mandatory_field(self):
        """
        Employee create without mandatory field should throw validation error
        :return:
        """
        # Hr user
        api_headers = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_minimum_fields)
            # without employee id
            del _data['employee_id']
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without joining date
            del _data['joining_date']
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_member)
            # without joining date
            del _data['nationality_code']
            res, code = h.create_employee(api_headers, _data)

    def test_employee_create_validation_error_custom_validator(self):
        """
        Test custom validator
        :return:
        """
        # Test first_name not_empty validator and custom validator
        # Hr user
        api_headers = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without employee id
            _data['joining_date'] = "1992/01/01"
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without employee id
            _data['joining_date'] = "1992-01-01"
            _data['first_name'] = ""
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without employee id
            _data['work_country_code'] = "asdassda"
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without employee id
            del _data['work_country_code']
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            _data = copy.deepcopy(create_data.test_data_created_by_hr)
            # without employee id
            _data['graduation_level'] = "masasdasdter"
            res, code = h.create_employee(api_headers, _data)

        with self.assertRaises(core_err.ValidationError):
            res, code = h.create_employee(api_headers, create_data.test_data_member_role_link_error)

    def test_employee_show(self):
        """
        Test employee show. Data is different for different user types
        :return:
        """
        # Create an employee member
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        api_headers_hr = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        api_headers_member = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        employee_id = create_data.test_data_member_role['employee_id']
        res, code = h.create_employee(api_headers_admin, create_data.test_data_member_role)
        self.assertEqual(code, 200)

        # ********* Employee view by admin -> others profile
        res, code = h.show_employee(api_headers_admin, {"id": employee_id})
        self.assertEqual(code, 200)
        expected_keys = h.get_schema_keys_given_role("show", "admin")
        result = h.delete_keys_from_employee_show(res['result'], del_keys=('id', 'created_at', 'updated_at'))
        actual_keys = set([x for x in result])
        self.assertFalse(expected_keys.difference(actual_keys) or actual_keys.difference(expected_keys))

        # ********* Employee view by hr -> others profile
        res, code = h.show_employee(api_headers_hr, {"id": employee_id})
        self.assertEqual(code, 200)
        expected_keys = h.get_schema_keys_given_role("show", "hr")
        result = h.delete_keys_from_employee_show(res['result'], del_keys=('id', 'created_at', 'updated_at'))
        actual_keys = set([x for x in result])
        self.assertFalse(expected_keys.difference(actual_keys) or actual_keys.difference(expected_keys))

        # ********* Employee view by member -> others profile
        res, code = h.show_employee(api_headers_member, {"id": employee_id})
        self.assertEqual(code, 200)
        expected_keys = h.get_schema_keys_given_role("show", "all")
        result = h.delete_keys_from_employee_show(res['result'], del_keys=('id', 'created_at', 'updated_at'))
        actual_keys = set([x for x in result])
        self.assertFalse(expected_keys.difference(actual_keys) or actual_keys.difference(expected_keys))

        # ********* Employee view by member -> his/her own profile
        res, code = h.show_employee(api_headers_member, {"id": employee_id})
        self.assertEqual(code, 200)
        _email = res['result']['work_email']
        api_key, _key = h.get_api_key(email=_email)
        api_headers_self = {
            "HTTP_API_KEY": _key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        res, code = h.show_employee(api_headers_self, {"id": employee_id})
        self.assertEqual(code, 200)
        expected_keys = h.get_schema_keys_given_role("show", "member")
        result = h.delete_keys_from_employee_show(res['result'], del_keys=('id', 'created_at', 'updated_at'))
        actual_keys = set([x for x in result])
        self.assertFalse(expected_keys.difference(actual_keys) or actual_keys.difference(expected_keys))

    def test_employee_update_by_role(self):
        """
        Profiles with member role should not be allowed to update others profile
        :return:
        """
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_member = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_hr = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        # Create employee by admin
        data = copy.deepcopy(create_data.test_data_member_role)
        _email_id = data['work_email']
        _employee_id = data['employee_id']
        res, code = h.create_employee(api_headers_admin, data)
        self.assertEqual(code, 200)
        _id = res['result']["id"]

        # ***************** Case 1: employee update by member role
        with self.assertRaises(core_err.NotAuthorizedError):
            _data = copy.deepcopy(create_data.test_data_member_role)
            _update_data = {
                "id": _data['employee_id'],
                "first_name": "asdasdasd"
            }
            res, code = h.update_employee(api_headers_member, _update_data)

        # ***************** Case 2: employee update by self - update by employee id
        api_key, _key_self = h.get_api_key(email=_email_id)
        api_headers_self = {
            "HTTP_API_KEY": _key_self,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        _update_data = {
            "id": _employee_id,
            "first_name": "test_update_name"
        }
        res, code = h.update_employee(api_headers_self, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['first_name'], _update_data['first_name'])

        # ****************** Case 3: employee update by self - update by id
        _update_data = {
            "id": _id,
            "last_name": "test_update_name"
        }
        res, code = h.update_employee(api_headers_self, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['last_name'], _update_data['last_name'])

        # ****************** Case 4: employee update by admin
        _update_data = {
            "joining_date": '2010-07-09',
            "id": _employee_id
        }
        res, code = h.update_employee(api_headers_admin, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['joining_date'], _update_data['joining_date'])

        # ****************** Case 5: employee update by hr
        _update_data = {
            "nationality_code": 'es',
            "id": _employee_id
        }
        res, code = h.update_employee(api_headers_hr, _update_data)
        self.assertEqual(res['result']['nationality_code'], _update_data['nationality_code'])
        self.assertEqual(code, 200)

    def test_employee_update_employee_id(self):
        """
        Try changing employee_id by admin, member, hr and self
        :return:
        """
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_member = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_hr = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']
        _id = res['result']['id']
        _email = res['result']['work_email']

        # ***************** Case 1: change employee id by admin
        _update_data = {
            "id": _id,
            "employee_id": "DLX-test-123",
        }
        res, code = h.update_employee(api_headers_admin, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['employee_id'].lower(), _update_data['employee_id'].lower())

        # ***************** Case 2: change employee id by hr using employee id
        _update_data = {
            "id": "DLX-test-123",
            "employee_id": "DLX-test-1234",
        }
        res, code = h.update_employee(api_headers_hr, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['employee_id'].lower(), _update_data['employee_id'].lower())

        # ***************** Case 3: change employee id by member
        _update_data = {
            "id": _id,
            "employee_id": "DLX-test-1234567",
        }
        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.update_employee(api_headers_member, _update_data)

        # ***************** Case 4: change employee id by self
        api_key, _key = h.get_api_key(email=_email)
        api_headers_self = {
            "HTTP_API_KEY": _key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        _update_data = {
            "id": _id,
            "employee_id": "DLX-test-my-123",
        }
        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.update_employee(api_headers_self, _update_data)

    def test_employee_update_parameters(self):
        """
        Test employee update by different parameters
        :return:
        """
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_member = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_hr = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']
        _id = res['result']['id']

        # ***************** Case 1: update work_email, first_name and last_name by admin
        _update_data = {
            "id": _id,
            "last_name": "testmy_name",
            "work_email": "testmy_name@gmail.com"
        }
        res, code = h.update_employee(api_headers_admin, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['last_name'], _update_data['last_name'])
        self.assertEqual(res['result']['work_email'], _update_data['work_email'])

        # ***************** Case 2: update work_email and last_name by hr
        _update_data = {
            "id": _employee_id,
            "last_name": "testmy2_name",
            "work_email": "testmy2_name@gmail.com",
            "first_name": "testmy2_firstname"
        }
        res, code = h.update_employee(api_headers_hr, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['last_name'], _update_data['last_name'])
        self.assertEqual(res['result']['work_email'], _update_data['work_email'])
        self.assertEqual(res['result']['first_name'], _update_data['first_name'])

        # ***************** Case 3: change joining_date by self
        api_key, _key = h.get_api_key(email="testmy2_name@gmail.com")
        api_headers_self = {
            "HTTP_API_KEY": _key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        _update_data = {
            "id": _employee_id,
            "joining_date": "1992-07-09",
        }
        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.update_employee(api_headers_self, _update_data)

        # ***************** Case 4: change work_country_code by self
        _update_data = {
            "id": _employee_id,
            "work_country_code": "ie",
        }
        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.update_employee(api_headers_self, _update_data)

        _update_data = {
            "id": _employee_id,
            "position": "dev",
        }
        res, code = h.update_employee(api_headers_self, _update_data)
        self.assertEqual(res['result']['position'].lower(), _update_data['position'].lower())

        # ***************** Case 5: change bio by self
        _update_data = {
            "id": _employee_id,
            "bio": "My name is fun and this is new app",
        }
        res, code = h.update_employee(api_headers_self, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['bio'].lower(), _update_data['bio'].lower())

        # ****************** Case 6: Link error
        _update_data = {
            "id": _employee_id,
            "social_github": "iasdasde"
        }
        with self.assertRaises(core_err.ValidationError):
            res, code = h.update_employee(api_headers_self, _update_data)

        _update_data = {
            "id": _employee_id,
            "social_github": ""
        }
        res, code = h.update_employee(api_headers_self, _update_data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['social_github'].lower(), _update_data['social_github'].lower())

    def test_employee_delete(self):
        """
        Test employee delete
        :return:
        """
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_member = {
            "HTTP_API_KEY": self._member_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        api_headers_hr = {
            "HTTP_API_KEY": self._hr_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }

        # **************** Case 1: delete employee by admin employee id
        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']

        res, code = h.delete_employee(api_headers_admin, {"id": _employee_id})
        self.assertEqual(code, 200)
        with self.assertRaises(core_err.NotFoundError):
            res, code = h.show_employee(api_headers_admin, {"id": _employee_id})

        # **************** Case 2: delete employee by hr employee id
        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']

        res, code = h.delete_employee(api_headers_hr, {"id": _employee_id})
        self.assertEqual(code, 200)
        with self.assertRaises(core_err.NotFoundError):
            res, code = h.show_employee(api_headers_admin, {"id": _employee_id})

        # **************** Case 3: delete employee by member
        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']

        with self.assertRaises(core_err.NotAuthorizedError):
            res, code = h.delete_employee(api_headers_member, {"id": _employee_id})

        # **************** Case 4: delete employee by admin id
        _data = copy.deepcopy(create_data.test_data_created_by_hr)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _id = res['result']['id']

        res, code = h.delete_employee(api_headers_admin, {"id": _id})
        self.assertEqual(code, 200)
        with self.assertRaises(core_err.NotFoundError):
            res, code = h.show_employee(api_headers_admin, {"id": _id})

    def test_employee_create_with_avatar(self):
        """

        :return:
        """
        client = Client()
        api_url = "http://127.0.0.1/etmapp/api/employee_create"
        _dir = os.path.dirname(os.path.realpath(__file__))

        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key
            # default is multipart/form
        }
        _data = copy.deepcopy(create_data.test_data_created_by_hr)
        upload_avatar = open(os.path.join(_dir, "test_avtar.png"), "rb")
        _data['upload_avatar'] = upload_avatar
        response = client.post(api_url, _data, **api_headers_admin)
        self.assertEqual(200, response.status_code)

    def test_employee_update_avatar(self):
        """
        # Update and delete avatar
        :return:
        """
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        # **************** Case 1: update employee avatar
        _data = copy.deepcopy(create_data.test_data_member_role)
        res, code = h.create_employee(api_headers_admin, _data)
        self.assertEqual(code, 200)
        _employee_id = res['result']['employee_id']

        client = Client()
        api_url = "http://127.0.0.1/etmapp/api/update_employee"
        _dir = os.path.dirname(os.path.realpath(__file__))
        api_headers_admin = {
            "HTTP_API_KEY": self._admin_key
            # default is multipart/form
        }
        upload_avatar = open(os.path.join(_dir, "test_avtar.png"), "rb")
        _update_data = {
            "id": _employee_id,
            "upload_avatar": upload_avatar
        }
        response = client.post(api_url, _update_data, **api_headers_admin)
        self.assertEqual(200, response.status_code)

    def test_employee_create_with_non_mandatory_field(self):
        """
        Test employee create without mandatory field
        :return:
        """
        api_headers = {
            "HTTP_API_KEY": self._admin_key,
            'content_type': 'application/json; charset=UTF-8',
            'Accept': 'application/json'
        }
        _data = copy.deepcopy(create_data.test_data_member_role)
        _data['contact_address'] = "Dublin City center"
        _data['contact_address_2'] = "Blackrock"
        res, code = h.create_employee(api_headers, _data)
        self.assertEqual(code, 200)
        self.assertEqual(res['result']['contact_address'].lower(), _data['contact_address'].lower())
        self.assertEqual(res['result']['contact_address_2'].lower(), _data['contact_address_2'].lower())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Destroy the data setup in setUpClass
        :return: None
        """
        pass


