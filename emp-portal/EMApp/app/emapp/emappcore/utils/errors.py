
class BaseEMAppError(Exception):
    pass


class NotFoundError(BaseEMAppError):
    pass


class NotAuthorized(BaseEMAppError):
    pass


class ParameterError(BaseEMAppError):
    pass


class ValidationError(BaseEMAppError):
    pass


class AppPluginError(BaseEMAppError):
    pass


class MethodNotAllowed(BaseEMAppError):
    pass


class UserNotFound(BaseEMAppError):
    pass


class UnexpectedError(BaseEMAppError):
    pass


class NotAuthorizedError(BaseEMAppError):
    pass


class SchemaError(BaseEMAppError):
    pass


class NotSupported(BaseEMAppError):
    pass


class ParameterNotAllowed(BaseEMAppError):
    pass


class BadRequest(BaseEMAppError):
    pass


class InternalServerError(BaseEMAppError):
    pass
