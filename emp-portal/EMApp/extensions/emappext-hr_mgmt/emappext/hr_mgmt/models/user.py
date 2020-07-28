from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_api_key.models import APIKey
import uuid
import logging
log = logging.getLogger(__name__)


class BaseProfile(AbstractUser):
    """
    Enhancing user model with additional fields. This is in relation with a table ProfileExtras.
    Extras can be utilised to add any fields to further enhance Profile with key value pair.
    """
    email = None
    id = models.CharField(max_length=50, unique=True, blank=False, default=uuid.uuid4, editable=False, primary_key=True)
    date_of_birth = models.DateField(blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=False)
    nationality_code = models.CharField(max_length=10, blank=False)
    bio = models.TextField(blank=True)
    work_email = models.EmailField(max_length=100, blank=False, unique=True)
    graduation_level = models.CharField(max_length=50, blank=True)
    graduated_from = models.TextField(blank=True, null=True)
    graduated_year = models.DateField(blank=True, null=True)
    contact_ph = models.CharField(max_length=50, blank=True)
    contact_address = models.TextField(blank=True)
    contact_address_2 = models.TextField(blank=True)
    contact_country_code = models.CharField(max_length=10, blank=True)
    contact_postal_code = models.CharField(max_length=30, blank=True)
    social_linkedin = models.TextField(blank=True)
    social_github = models.TextField(blank=True)
    social_twitter = models.TextField(blank=True)
    avatar = models.ImageField(max_length=50, upload_to="avatar", blank=True)
    _api_key = models.OneToOneField(APIKey, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    EMAIL_FIELD = 'work_email'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['work_email'], name="work_email")
        ]

