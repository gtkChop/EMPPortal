from emappcore.utils import errors as e
import logging
log = logging.getLogger(__name__)


class _APIGetActions:
    """
    All api GET actions are registered here as static methods
    """
    pass


class _APIPutActions:
    """
    All api PUT actions are registered here as static methods
    """
    pass


class _APIPostActions:
    """
    All api POST actions are registered here as static methods
    """
    pass


class _APIDeleteActions:
    """
    All api DELETE actions are registered here as static methods
    """
    pass


class EMAppAPIActions:
    """
    On register new api, a static function is registered to a respective classes depends on the method type

    Attributes:
        _action_classes: (private) available api methods and its respective classes

    Methods:
        register: To register a new api function
    """
    _action_classes = {
        'get': _APIGetActions,
        'post': _APIPostActions,
        'put': _APIPutActions,
        'delete': _APIDeleteActions
    }

    def __init__(self):
        pass

    def __setattr__(self, key, value):
        raise ValueError("Not allowed to se attribute. Only static methods are allowed")

    @classmethod
    def _validate_method(cls, method):
        """
        Validates a method type

        :param method: Should be of any of get, put, post and delete and should be in lowercase
        :return:
        """
        if method and method.lower() in cls._action_classes:
            return True
        else:
            return False

    @classmethod
    def register(cls, action_name=None, action_func=None, method=None):
        """
        Api registration process which is done in register.py api_action method and
        it is a part of BaseAppCorePluginInterface.

        :param action_name: str api action name
        :param action_func: func function corresponding to action_name
        :param method: str get, put, post and delete
        :return: None
        """
        registration_type = "api"

        if not cls._validate_method(method):
            raise e.MethodNotAllowed("Only get, post, put, delete methods are allowed")

        if not action_name:
            raise e.AppPluginError("{} action name is required parameter".format(registration_type))

        if not action_func:
            raise e.AppPluginError("{} action_func is required parameter".format(registration_type))

        if not callable(action_func):
            raise e.AppPluginError("Api function given - {} is not callable - "
                                   "check registration.py file".format(action_name))

        if hasattr(cls, action_name):
            log.warning("Overwriting the existing api action: {}".format(action_name))
        else:
            log.info("Registering the {} action: {} for method".format(registration_type, action_name, method))

        try:
            setattr(cls._action_classes.get(method.lower()), action_name, staticmethod(action_func))
        except AttributeError:
            raise e.AppPluginError("Given api method not available. Supported api methods - get, post, put and delete")


class APIActions(EMAppAPIActions):
    """
    This api actions is for toolkit import and for using api as function. from emappcore.toolkit import api_action

    Only used to internal api calls within applications. Do not overwrite this.

    """

    def _run_action(self, action_class, action_name, app_context, data_dict):
        """
        Internal run api action given api name, api class, app context and parameters.

        :param action_class: class API action class
        :param action_name: str Action name
        :param app_context: dict app context contains user information and more.
        :param data_dict: dict api parameters
        :return: calls respective registered function
        """
        log.info("Executing an api action: {}".format(action_name))
        if not hasattr(action_class, action_name):
            raise e.NotFoundError("API action not found")

        return getattr(action_class, action_name)(app_context, data_dict)

    def get_actions(self, action_name, app_context, data_dict):
        """
        Used to call API GET actions

        :param action_name: str Action name
        :param app_context: dict app context contains user information and more.
        :param data_dict: dict api parameters
        :return: func _run_action
        """
        return self._run_action(self._action_classes.get("get"), action_name, app_context, data_dict)

    def post_actions(self, action_name, app_context, data_dict):
        """
        Used to call API POST actions

        :param action_name: str Action name
        :param app_context: dict app context contains user information and more.
        :param data_dict: dict api parameters
        :return: func _run_action
        """
        return self._run_action(self._action_classes.get("post"), action_name, app_context, data_dict)

    def put_actions(self, action_name, app_context, data_dict):
        """
        Used to call API PUT actions

        :param action_name: str Action name
        :param app_context: dict app context contains user information and more.
        :param data_dict: dict api parameters
        :return: func _run_action
        """
        return self._run_action(self._action_classes.get("put"), action_name, app_context, data_dict)

    def delete_actions(self, action_name, app_context, data_dict):
        """
        Used to call API DELETE actions

        :param action_name: str Action name
        :param app_context: dict app context contains user information and more.
        :param data_dict: dict api parameters
        :return: func _run_action
        """
        return self._run_action(self._action_classes.get("delete"), action_name, app_context, data_dict)
