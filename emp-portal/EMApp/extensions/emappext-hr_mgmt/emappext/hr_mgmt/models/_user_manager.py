from django.contrib.auth.base_user import BaseUserManager
import logging
log = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.

    Methods:
        create_user: creates a new user
        create_superuser: Creates a new super user.

    """
    def create_user(self, password, **fields):
        """
        Create and save a User with the given email and password.
        """
        fields['work_email'] = self.normalize_email(fields['work_email'])
        user = self.model(**fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_active', True)
        if fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(password, **fields)
