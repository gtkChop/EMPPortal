from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from emappext.hr_mgmt.models import Employee

admin.site.unregister(Group)
admin.site.register(Employee, UserAdmin)
