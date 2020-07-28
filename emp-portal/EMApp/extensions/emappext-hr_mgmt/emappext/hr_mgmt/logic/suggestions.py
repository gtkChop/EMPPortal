from elasticsearch import exceptions
from emappcore.utils import errors as err
from emappext.hr_mgmt.utils import auth
from emappext.hr_mgmt.index.employee_index import EmployeeDocument
import logging

log = logging.getLogger(__name__)


def suggestion_employee_index(app_context, data_dict):
    """
    Get suggestions for the given field and search value
    :param app_context: dict
    :param data_dict: dict
    :return: dict
    """
    auth.is_authenticated(app_context)
    _value = data_dict.get('search[term]', '')
    _search_field = data_dict.get('search_field', '')
    _limit = 30
    log.info("getting suggestion for term: {}".format(_value))
    log.info("Given suggestion field: {}".format(_search_field))

    if not _search_field or not _value:
        return []

    _search_field = _search_field.split("-")[-1]

    _search = EmployeeDocument.search()

    try:
        sugg = _search.suggest(
            '{}'.format(_search_field),
            _value, completion={
                'field': '{}.suggest'.format(_search_field)
            }
        )
        suggestions = sugg.execute()
        options = getattr(suggestions.suggest, _search_field)[0]['options'][:_limit]
        result = []
        _val_check = []
        for r in options:
            _sug = r['text']
            if _sug.lower().strip() not in _val_check:
                result.append(
                    {
                        "id": _sug.lower().strip(),
                        "text": _sug.strip().title()
                    }
                )
                _val_check.append(_sug.lower().strip())

        return result
    except exceptions.RequestError as e:
        log.error(e)
        log.error("Please verify the given field")
        raise err.ValidationError({
            _search_field: "Looks like field is not available in index"
        })

    except Exception as e:
        log.error(e)
        log.error("Error not handles in suggestion employee")

