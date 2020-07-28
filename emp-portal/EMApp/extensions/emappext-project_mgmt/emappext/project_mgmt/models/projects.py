from django.db import models
from emappext.hr_mgmt.models import Employee
from emappext.project_mgmt.models.department import Department
import uuid
import logging

log = logging.getLogger(__name__)


class Projects(models.Model):
    """
    Each individual projects are stored in this table.
    """
    project_title = models.CharField(max_length=300, blank=False)
    project_id = models.CharField(max_length=50, db_index=True, blank=False, unique=True, default=str(uuid.uuid4()))
    project_description = models.TextField(blank=False)
    project_type = models.CharField(max_length=100, blank=False)
    contract_start_date = models.DateField(blank=False)
    contract_end_date = models.DateField(blank=False)
    client_name = models.CharField(max_length=300, blank=True)
    client_point_of_contact_email = models.EmailField(max_length=50, blank=True)
    client_point_of_contact_name = models.CharField(max_length=30, blank=True)
    project_tasks_link = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        'project_title',
        'project_id',
        'project_description',
        'project_type',
        'contract_start_date',
        'contract_end_date',
        'department'
    ]

    def __str__(self):
        return self.project_description


class ProjectsExtras(models.Model):
    """
    Any extra items related to the projects are stored in this table
    """
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=False)
    value = models.TextField(blank=False)


class ProjectMembers(models.Model):
    """
    All the project members tagged to a project are stored in this table.
    This will be populated when extra items are added to the core project schema.
    """
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        'project',
        'employee',
        'is_manager'
    ]

    def __str__(self):
        return "Employee id: {} and project: {}".format(self.project.employee_id, self.project.project_title)
