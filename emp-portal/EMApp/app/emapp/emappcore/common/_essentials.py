from emappcore.utils import errors as err
from jsonschema import validate as _validate
import importlib
import copy
import os
import json
import logging
log = logging.getLogger(__name__)


def _register_static_methods(cls, registration_type, name, func):
    """
    To register static methods to a given class. For internal user only.

    :param cls: class
    :param registration_type: str
    :param name: str
    :param func: function
    :return: None
    """
    if not name:
        raise err.AppPluginError("{} name is required parameter".format(registration_type))

    if not func:
        raise err.AppPluginError("{} func is required parameter".format(registration_type))

    if hasattr(cls, name):
        log.warning("Overwriting the existing {} function: {}".format(registration_type, name))
    else:
        log.info("Registering the {}: {}".format(registration_type, name))

    if not callable(func):
        raise err.AppPluginError("Given function {} - "
                                 "is not callable - check plugin for {}".format(name, registration_type))

    setattr(cls, name, staticmethod(func))


class EMAppConfig(dict):
    """
    This is the config class for this app which is inherited from dict. It can be accessed through
    emappcore.common - config.

    Disabled run time changing config hence, cannot set attribute during run time.

    """

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError("Not allowed to modify the attribute")
        else:
            dict.__setattr__(self, key, value)

    def __setitem__(self, key, value):
        if key in self.keys():
            raise ValueError("Not allowed to modify the dictionary")
        else:
            dict.__setitem__(self, key, value)

    def __delattr__(self, item):
        raise AttributeError("Not allowed to delete attribute: {}".format(item))

    def __delitem__(self, key):
        raise KeyError("Not allowed to delete item: {}".format(key))

    def popitem(self):
        raise ValueError("Not allowed to pop last item.")

    def pop(self, k):
        raise KeyError("Not allowed")


class EMAppUtilities:
    """
    All apps utilities functions are registered here. This class will be available in
    BaseAppCorePluginInterface.app_helpers().

    Utilities functions are available at from emappcore.common import utilities

    Methods:

        register: (classmethod) This used to register any new utilities functions and are
                  available in BaseAppCorePluginInterface.app_helpers()
    """

    @classmethod
    def register(cls, name=None, func=None):
        """
        Register any new utilities functions.

        :param name: str (Utility function name)
        :param func: function (Utility function)
        :return: None
        """
        _register_static_methods(cls, "utility", name, func)


class EMAppValidators:
    """
    All apps validators functions are registered here. This class will be available in
    BaseAppCorePluginInterface.app_validators().

    Validator functions are available at from emappcore.common import validators.
    Registered validators can also be used in schema as space separated strings

    Methods:

        register: (classmethod) This used to register any new validators function
                  and available in BaseAppCorePluginInterface.app_validators()
    """

    @classmethod
    def register(cls, name=None, func=None):
        """
        Register any new validator functions.

        :param name: str (Validator function name)
        :param func: function (Validator function
        :return: None
        """
        _register_static_methods(cls, "validator", name, func)


class EMAppSchemas(EMAppValidators):
    """
    Responsible in register, validate and fetch schemas. This class will be available in
    BaseAppCorePluginInterface.app_schema().

    :methods

    get_schema: Gets the content of the schema given name
    validate: Responsible to validate the contents against the given schema name

    Methods:

        register: (classmethod) This used to register any new schema and
                   available in BaseAppCorePluginInterface.app_schema()
    """

    def get_schema(self, schema_name):
        """
        This will get the schema contents given schema name.
        :param schema_name: str (registered schema name)
        :return: dict (schema content)
        """
        return copy.deepcopy(getattr(self, "_{}".format(schema_name)))

    def validate(self, schema_name, data_dict):
        """
        Step 1: Validate the json-schema
        Step 2: Validate custom validations given in the schema files
        Step 3: If validators given and also the available options. Validation options

        Note 1: If no validators given but options are available, then considers it to be possible emtpy values.
        Note 2: If not validators given is same as ignore missing values.


        :param schema_name: str (Name of the schema)
        :param data_dict: dict (All the values associated with the schema)
        :return: None (Raises errors if any validation errors)
        """

        log.info("Validating the data against given schema - {}".format(schema_name))
        schema = self.get_schema(schema_name)

        diff = set(data_dict.keys()).difference(set(schema['properties']))
        if diff:
            raise err.ValidationError({
                "parameter": "Not allowed parameter: {}".format(list(diff)[0])
            })

        try:
            _validate(
                instance=data_dict,
                schema=schema
            )
        except Exception as e:
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = "InternalServerError"
            raise err.ValidationError({"ValidationError": msg})

        log.info("Validating all the data given")
        for key in schema['properties']:

            # Custom Validators
            _validators_string = schema['properties'][key]['validators'].strip()
            _options = schema['properties'][key].get('options', '')
            _given_value = data_dict.get(key, '')

            if _validators_string:
                _validators = _validators_string.split(" ")
                for _validator in _validators:
                    if _validator == "ignore_missing" and not _given_value:
                        break
                    else:
                        getattr(self, _validator.strip())(key, data_dict[key])

            if _options and _given_value not in (x['value'] for x in _options):
                if not _given_value and "ignore_missing" in _validators_string:
                    pass
                else:
                    # Check for options
                    raise err.ValidationError({
                        key: "Given value does not match the available options"
                    })

        return True

    @classmethod
    def register(cls, schema_dir=None, file_name=None, schema_name=None):
        """
        This will be utilised in registering any new schema that needs to be added to the application.
        Any schema added will be available in emappcore.common.schemas.

        :param schema_dir: str (Schema directory as module <>.<>.schemas).
        :param file_name: (Schema file name. This should be available in schema directory).
        :param schema_name: (Name of the schema that to be registered and can be utilised to access schema content).
        :return: None
        """
        log.info("Registering the schema - {}".format(schema_name))
        try:

            schema_dir_path = importlib.import_module(schema_dir).__path__[0]
            schema_file = os.path.join(schema_dir_path, file_name)
            log.info("Given schema path")
            log.info(schema_file)

            if not os.path.isfile(schema_file):
                raise err.AppPluginError("Schema file not found")

            log.info("Found schema - {}".format(schema_file))

            with open(schema_file, 'r') as sh:
                schema_content = json.load(sh)
                sh.close()

            if schema_content:
                if hasattr(cls, "_{}".format(schema_name)):
                    log.warning("Overwriting the existing schema - {}".format(schema_name))
                setattr(cls, "_{}".format(schema_name), schema_content)
                log.info("Registering schema - {}".format(schema_name))

        except ModuleNotFoundError as e:
            log.error(e)
            raise err.AppPluginError("Schema error verify schema parameter")




