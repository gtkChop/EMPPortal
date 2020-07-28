from django.shortcuts import render


def abort(request, code=None, error_message=None, error_title=None):
    """
    App abort page with error code and error message
    :param request: django request object
    :param code: int
    :param error_message: str
    :param error_title: str
    :return: template
    """
    extra_vars = {
        "code": code,
        "error_message": error_message,
        "error_title": error_title
    }
    return render(request, 'utils/abort.html', extra_vars)


def server_error(request, code=500, error_message="Something went wrong!!"):
    """
    Internal server error template
    :param request: django request object
    :param code: int
    :param error_message: str
    :return: template
    """
    extra_vars = {
        "code": code,
        "error_message": error_message
    }

    return render(request, 'utils/server_error.html', extra_vars)
