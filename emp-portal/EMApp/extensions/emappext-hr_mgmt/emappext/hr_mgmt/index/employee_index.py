from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from emappcore.tools.analyzers import trigram_analyzer, email_analyzer
from emappext.hr_mgmt.models import Employee
import logging

log = logging.getLogger(__name__)


@registry.register_document
class EmployeeDocument(Document):

    first_name = fields.TextField(
        attr='first_name',
        analyzer=trigram_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    middle_name = fields.TextField(
        attr='middle_name',
        analyzer=trigram_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    last_name = fields.TextField(
        attr='last_name',
        analyzer=trigram_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    work_email = fields.TextField(
        attr='work_email',
        analyzer=email_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    skills = fields.TextField(
        attr='skills',
        analyzer=trigram_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    employee_id = fields.TextField(
        attr='employee_id',
        analyzer=trigram_analyzer,
        fields={
            'suggest': fields.Completion(),
        }
    )

    position = fields.TextField()
    work_country_code = fields.TextField()
    id = fields.KeywordField()

    class Index:
        name = 'employee'
        doc_type = '_doc'

    class Django:
        model = Employee

    @staticmethod
    def default_search_fields_full_text():
        """
        Default searchable fields
        :return: tuple
        """
        default_search_fields = (
            "first_name",
            "middle_name",
            "last_name",
            "work_email",
            "employee_id",
            "position",
            "work_country_code"
        )
        return default_search_fields

    def as_dict(self):
        """
        Convert the index data to dictionary
        :return:
        """
        result = dict()
        _fields = self.default_search_fields_full_text()
        for _field in _fields:
            result[_field] = getattr(self, _field)

        result['id'] = getattr(self, "id")

        return result
