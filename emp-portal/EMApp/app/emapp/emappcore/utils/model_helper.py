from emappcore.utils import errors as err
import datetime
import json
import logging

log = logging.getLogger(__name__)


def create_extras_table_values(extras_model=None, connecting_key=None,
                               connecting_model=None, key=None, value=None):
    """
    Populate model with extra values. The logic is the schema key doesnt contain in core db table,
    all the items are added as key value pair in extras table.

    Note: All the value field is converted into text field. All the is done through django transaction

    :param extras_model: model class
    :param connecting_key: str
    :param connecting_model: model instance
    :param key: str
    :param value: str, dict, list, tuple, int, float
    :return: None
    """

    allowed_data_types = (
        "str", 'dict', 'tuple', "list", 'int', "float"
    )

    if type(value).__name__ not in allowed_data_types:
        raise err.NotSupported({
            'model_extras_data_insert_error': "Type of data is not supported for extras table. Check the value."
        })

    if type(value).__name__ in ("str", 'dict', 'tuple', "list"):
        value = json.dumps(value)
    else:
        value = str(value)

    model_extra = extras_model()
    setattr(model_extra, connecting_key, connecting_model)
    setattr(model_extra, "key", key)
    setattr(model_extra, "value", value)

    return model_extra


def model_dictize(db_models=None, db_extras=None, schema=None):
    """
    This will extract all the necessary information for the connected db models.

    Note: Extras tables are stored as key value pair and all the data is string/json.

    :param db_models: tuple (items is of type django model instance)
    :param db_extras: tuple (items is of type django model instance)
    :param schema: dict
    :return: dict
    """
    result_dict = dict()
    for _property in schema['properties']:
        # Main models
        for _model in db_models:
            if hasattr(_model, _property):
                _val = getattr(_model, _property)
                if _val is None:
                    _val = ''
                if isinstance(_val, datetime.date):
                    _val = str(_val)
                result_dict[_property] = _val
                break

        # This is for extra tables.
        for _extra in db_extras:
            for row in _extra:
                if row and row.key == _property:
                    if isinstance(row.value, str):
                        try:
                            result_dict[_property] = json.loads(row.value)
                        except ValueError:
                            result_dict[_property] = row.value
                    break
    return result_dict


def clean_data_dict_for_api_calls(data_dict, params_to_delete=None):
    """
    Removed the keys from data dict given parameter. Internal use only
    :param data_dict: dict
    :param params_to_delete: tuple
    :return: dict
    """
    try:
        del data_dict['csrfmiddlewaretoken']
    except KeyError:
        pass

    if not params_to_delete:
        return data_dict

    for key in params_to_delete:
        try:
            del data_dict[key]
        except KeyError:
            pass
    return data_dict
