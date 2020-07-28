from django.db import models
from emappext.project_mgmt.models.projects import Projects
from emappext.hr_mgmt.models.employee import Employee
import uuid
import logging

log = logging.getLogger(__name__)


class Tasks(models.Model):
    """
    Each project member task details are stored in this table
    """
    task_date = models.DateField(blank=False)
    task_id = models.CharField(max_length=20, db_index=True, blank=False, unique=True, default=str(uuid.uuid4()))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    task_summary = models.TextField(blank=False)
    task_comments = models.TextField(blank=True)
    task_link = models.URLField(max_length=200, blank=False)
    task_type = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        'task_date',
        'employee',
        'project',
        'employee',
        'task_summary',
        'task_type'
    ]

    class Meta:
        ordering = ['-task_date']

    def __str__(self):
        return self.task_summary


class TasksExtras(models.Model):
    """
    Any extra items related to the task are stored in this table.
    This will be populated when extra items are added to the core task schema.
    """
    tasks = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, blank=False)
    value = models.TextField(blank=False)
