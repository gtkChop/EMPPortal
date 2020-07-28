from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from emappcore.tools import api_action
from emappcore.utils import errors as err
from emappcore.common import utilities as u
import collections
import json
import logging

log = logging.getLogger(__name__)


class EMAppAPIView(APIView):
    """
    View function for all api. This will return json response.
    If any errors, suitable error message will be sent as json response.

    Methods:

        api_response: This is as view function and is added in url dispatcher
        _prepare_api_context: (private) Builds context for the api functions
        _parse_api_parameters: (private) Get all parameters or query string from the request to dictionary
        _send_success_response: (private) Prepares a data from api return and returns as json response
        _send_error_response: (private) Prepares a error data from api return and returns as json response

    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [HasAPIKey | IsAuthenticated]

    @staticmethod
    def _prepare_api_context(request=None, action_name=None):
        """
        Prepare a context to be sent to the api.

        Note 1: If the user is already logged in. User object is extracted from request
        Note 2: If not logged in try to get api key from the request parameter

        :param request: django request object
        :return: dict
        """
        if "application/json" not in (request.META.get('CONTENT_TYPE', '') or request.META.get('content_type', '')):
            # check if its a 'multipart/form-data
            if "multipart/form-data" in (request.META.get('CONTENT_TYPE', '') or request.META.get('content_type', '')):
                pass
            else:
                raise err.BadRequest({
                    "headers": "Headers are not set Content-type: application/json is required"
                })

        log.info("Building api context")
        context = {
            "api_action": action_name,
            "type": "api",
            "user": request.user,
            "files": request.FILES,
            "is_superuser": False,
            "role": ""
        }

        if "HTTP_API_KEY" in request.META or "X-API_KEY" in request.headers:
            log.info("Found api key. Fetching user")
            _key = request.META.get('HTTP_API_KEY', '') or request.headers.get('X-API_KEY', '')
            try:
                api_key = APIKey.objects.get_from_key(_key)

                if api_key.is_valid(_key):
                    context['user'] = api_key.baseprofile.employee
                    context['is_superuser'] = context['user'].is_superuser
                    context['role'] = context['user'].role if hasattr(context['user'], "role") else ""
                    if context['is_superuser']:
                        context['role'] = "admin"
            except APIKey.DoesNotExist:
                pass
        return context

    @staticmethod
    def _parse_api_parameters(request):
        """
        Responsible to parse all the parameters to send to api as data_dict.
        Parses parameters from the django request for a suitable methods.

        :param request: django request instance
        :return: dict
        """

        log.info("Preparing api parameters")
        if request.META.get('CONTENT_LENGTH', '') and "application/json" in (
                request.META.get('CONTENT_TYPE', '') or request.META.get('content_type', '')):
            data_dict = json.loads(request.body)
        else:
            data_dict = u.convert_request_data_to_dict(getattr(request, request.method))

        return data_dict

    @staticmethod
    def _send_error_response(error_cls):
        """
        Responsible to parse the send thejson response with suitable error type and message.

        :param error_cls: instance (Error instance raised from  _send_success_response)
        :return: json
        """
        log.info("Sending error response")
        error_type = error_cls.__class__.__name__

        if error_type in ("BadRequest", ):
            status_code = 400
        elif error_type in ("NotFoundError", "UserNotFound"):
            status_code = 404
        elif error_type == ("ValidationError", "ParameterError", "ParameterNotAllowed", "MethodNotAllowed"):
            status_code = 409
        elif error_type in ("NotAuthorized", ):
            status_code = 401
        else:
            status_code = 500

        args = error_cls.args
        msg = None

        if args:
            msg = args[0]
        result = collections.OrderedDict({
            "status": "error",
            "error_type": error_type,
            "msg": msg or "unknown"
        })
        # Send 200 for errors
        # Give custom error message for application level validation errors
        return JsonResponse(result, status=status_code)

    def _send_success_response(self, method=None, action_name=None, context=None, data_dict=None):
        """
        Access API function for a request method and send the response as json.

        Raises a suitable errors and send the error response.

        :param method: str (Used to get api function for a suitable request method)
        :param action_name: (Action name of the api that is registered)
        :param context: dict (Contains information on user and their role)
        :param data_dict: (All url parameters as dict)
        :return: Json
        """

        response = collections.OrderedDict({
            "status": "success",
            "action_name": action_name
        })

        try:
            log.info("Given api action: {}".format(action_name))
            func = getattr(api_action, "{}_actions".format(method))
            api_result = func(action_name, context, data_dict)

            if isinstance(api_result, list):
                response['count'] = len(api_result)

            response['result'] = api_result

            return JsonResponse(response, status=200)
        except Exception as e:
            # Send error response
            log.error(e)
            return self._send_error_response(e)

    def dispatch(self, request, *args, **kwargs):
        """
        This is the view function for API response.
        :param request: django request object
        :return: json
        """
        action_name = kwargs.get('action_name', '')
        log.info("Requested api action: {}".format(action_name))
        try:
            context = self._prepare_api_context(
                request=request,
                action_name=action_name
            )
            data_dict = self._parse_api_parameters(request)

            request_method = request.method.lower()

            return self._send_success_response(
                method=request_method,
                action_name=action_name,
                context=context,
                data_dict=data_dict
            )
        except Exception as e:
            return self._send_error_response(e)
