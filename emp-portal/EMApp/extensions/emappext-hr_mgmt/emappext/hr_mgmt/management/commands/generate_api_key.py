from django.core.management.base import BaseCommand, CommandError
from rest_framework_api_key.models import APIKey
from emappext.hr_mgmt.models import Employee
import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate API key for the given work_email'

    def add_arguments(self, parser):
        parser.add_argument('work_email', type=str)

    def handle(self, *args, **options):
        """
        Handle the api key generation here. First check if the user exists if not raise validation error
        :param args:
        :param options:
        :return:
        """
        _email_id = options['work_email']
        log.info("Given email id: {}".format(_email_id))

        if not _email_id:
            raise CommandError({
                "work_email": "This field should be given"
            })

        try:
            APIKey.objects.filter(name=_email_id).delete()
        except Exception as e:
            pass

        api_key, key = Employee.generate_api_key(_email_id)
        log.info(api_key)
        log.info("Generated key: {}".format(key))
        log.info("You might need to same the key for the later user")
