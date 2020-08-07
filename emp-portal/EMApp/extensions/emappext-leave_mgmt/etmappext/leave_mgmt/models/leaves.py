from django.db import models
from emappcore.common import validators
from emappext.hr_mgmt.models import Employee
import uuid
import logging
log = logging.getLogger(__name__)

class EmployeeLeaves(models.Model):
    """
    The database tables to store employee leaves and its data
    """

    id = models.CharField(max_length=50, unique=True, blank=False, default=uuid.uuid4,
                          editable=False, primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    from_date = models.DateField(blank=False)
    to_date = models.DateField(blank=False)
    leave_type = models.CharField(max_length=1, blank=False)
    comments = models.TextField(blank=True)
    need_approval = models.BooleanField(default=True, blank=False)
    approval_from = models.ForeignKey(Employee, blank=True, on_delete=models.SET_NULL)
    approver_comments = models.TextField(blank=True)
    leave_status = models.CharField(max_length=1, blank=False, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)



