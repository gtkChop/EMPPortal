from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager
from rest_framework_api_key.models import APIKey
from emappcore.utils import model_helper, errors as err
from emappcore.common import schemas
from emappext.hr_mgmt.models._user_manager import CustomUserManager
from emappext.hr_mgmt.models.user import BaseProfile
import logging
log = logging.getLogger(__name__)


class Employee(BaseProfile):
    """
    Employee table containing all the employee information.
    """
    employee_id = models.CharField(max_length=100, blank=False, unique=True)
    joining_date = models.DateField(blank=False)
    position = models.CharField(max_length=100, blank=False)
    work_address = models.TextField(blank=False)
    work_country_code = models.CharField(max_length=10, blank=False)
    work_ph = models.CharField(max_length=100, blank=True)
    skills = ArrayField(models.CharField(max_length=50), size=30, default=list)
    experience = models.CharField(max_length=10, blank=True)
    reporting_manager = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, blank=False)

    REQUIRED_FIELDS = [
        'date_of_birth',
        'first_name',
        'last_name',
        'work_email',
        'nationality_code',
        'role',
        'employee_id',
        'joining_date',
        'position',
        'work_country_code',
        'work_address'
    ]

    objects = CustomUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee_id'], name="employee_id")
        ]

    def __str__(self):
        return "{} {}".format(self.employee_id, self.id)

    def save(self, *args, **kwargs):
        """
        Clean the data before saving to the database also generate api key if no key
        :param args:
        :param kwargs:
        :return:
        """
        self.username = self.normalize_username(self.username)
        self.work_email = BaseUserManager.normalize_email(self.work_email)

        if self.reporting_manager:
            try:
                _reporting_manager = Employee.get_employee_by_email(self.reporting_manager)
            except err.NotFoundError:
                log.error(self.reporting_manager)
                raise err.ValidationError({
                    "reporting_manager": "Given reporting manager not available"
                })
            if _reporting_manager.id == self.id:
                raise err.ValidationError({
                    "reporting_manager": "You cannot assign yourself as reporting manager"
                })
            self.reporting_manager = _reporting_manager.id

        if not hasattr(self, "_api_key") or not getattr(self, "_api_key"):
            log.info("Creating a new api key")
            api_key, key = APIKey.objects.create_key(name=self.work_email)
            self._api_key = APIKey.objects.get_from_key(key)

        _fields = (
            "employee_id",
        )
        for _field in _fields:
            val = getattr(self, _field)
            if val:
                setattr(self, _field, val.lower().strip())

        if not self.graduated_year:
            self.graduated_year = None

        # TODO default array doesnt work - Hack
        if not getattr(self, "skills"):
            self.skills = list()

        return super(self.__class__, self).save(*args, **kwargs)

    @classmethod
    def get_employee_by_email(cls, email_id):
        """
        Gte employee by email id
        :param email_id: str
        :return: employee object
        """
        log.info("Getting a employee instance for a email id: {}".format(email_id))
        _employees = cls.objects.filter(work_email__iexact=email_id)

        if not _employees:
            raise err.NotFoundError({
                "employee_id_or_id": "Employee not found."
            })
        if len(_employees) > 1:
            raise err.InternalServerError({
                "employee_id": "Multiple employees for a given id"
            })
        return _employees[0]

    @classmethod
    def get_employee_by_id(cls, emp_id):
        """
        Get employee by id or employee_id
        :param emp_id: str
        :return: django model instance
        """
        log.info("Getting a employee instance for a id: {}".format(emp_id))
        _employees = cls.objects.filter(id=emp_id) or cls.objects.filter(
            employee_id__iexact=emp_id) or cls.objects.filter(username__iexact=emp_id)

        if not _employees:
            raise err.NotFoundError({
                "employee_id_or_id": "Employee not found."
            })
        if len(_employees) > 1:
            raise err.InternalServerError({
                "employee_id": "Multiple employees for a given id"
            })
        return _employees[0]

    @classmethod
    def generate_api_key(cls, email):
        """
        Generate API key given the user/work email
        :param email: str
        :return: tuple
        """
        try:
            _profile = cls.objects.get(work_email=email)
        except Employee.DoesNotExist:
            raise err.ValidationError({
                "work_email": "No user found for the given work email"
            })

        log.info("Generating API key for an email: {}".format(email))
        try:
            APIKey.objects.filter(name=email).delete()
        except Exception as e:
            log.error(e)
            pass

        api_key, key = APIKey.objects.create_key(name=email)
        _profile._api_key = APIKey.objects.get_from_key(key)
        _profile.save()

        return api_key, key

    def _as_dict(self):
        """
        This for internal use only. The dict will not contain created_at, updated_at and id parameters
        :return:
        """
        log.info("Extracting employee data from the database")
        _schema = schemas.get_schema('employee_schema')
        schema_data = model_helper.model_dictize(
            db_models=(
                self,
            ),
            db_extras=(
                EmployeeExtras.objects.filter(employee=self),
            ),
            schema=_schema
        )
        schema_data['employee_id'] = schema_data['employee_id'].upper()
        return schema_data

    def as_dict(self):
        """
        Get database data for an employee given employee id or unique id
        :return: dict
        """
        schema_data = self._as_dict()
        schema_data["id"] = self.id
        schema_data['created_at'] = str(self.created_at)
        schema_data['updated_at'] = str(self.updated_at)

        try:
            schema_data['avatar'] = self.avatar.url
        except Exception as e:
            log.info(e)
            schema_data['avatar'] = ''

        return schema_data


class EmployeeExtras(models.Model):
    """
    Any extra employee related items are added here.
    This will be used if the schema is modified and any extra employee items are added here.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=False)
    value = models.TextField(blank=False)
