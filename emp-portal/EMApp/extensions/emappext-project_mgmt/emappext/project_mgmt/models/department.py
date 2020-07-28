from django.db import models
from emappext.hr_mgmt.models.employee import Employee


class Department(models.Model):
    """
    Department in a company/corporation. Holds all the data related to the department.
    """
    department_id = models.CharField(max_length=30, blank=False, db_index=True, unique=True)
    title = models.CharField(max_length=50, blank=False)
    short_name = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=False)
    department_head = models.OneToOneField(Employee, on_delete=models.PROTECT)

    REQUIRED_FIELDS = [
        'department_id',
        'title',
        'description',
        'department_head',
        'location'
    ]

    def __str__(self):
        return self.title


class DepartmentExtras(models.Model):
    """
    Any extra items related to the department are store in this table.
    This will be populated when extra items are added to the core department schema.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=False)
    value = models.TextField(blank=False)
