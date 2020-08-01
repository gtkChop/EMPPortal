from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from emappcore.utils import errors as err, model_helper
from emappcore.tools import api_action
from emappcore.common import abort, server_error, schemas, utilities as u
from emappext.hr_mgmt.utils import auth
from emappext.hr_mgmt import models
import logging

log = logging.getLogger(__name__)


@method_decorator([login_required], name='dispatch')
class EmployeeProfileView(View):
    """
    View class for profile/Employee view. This is used inhj /profile/<> page.
    Notes:
        - The fields are access controlled and access is defined in show and update keys in employeeP_schema.json file
        - Utilizes the api show_employee to fetch the required data
    """
    def get(self, request, profile_id=None):
        """
        View to show user profile. If profile_id=None, then the profile page for logged in user
        :return: render page
        """
        if profile_id == request.user.id:
            return redirect('profile')

        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role
        }
        extra_vars = dict()
        try:
            user_data = api_action.get_actions(
                "show_employee",
                context,
                {
                    "id": profile_id or request.user.username
                }
            )
            extra_vars['profile'] = user_data
            extra_vars["schema"] = schemas.get_schema("employee_schema")
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to see the page")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            messages.error(request, 'Requested user not available')
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return render(request, 'profile/read.html', extra_vars)


@method_decorator([login_required], name='dispatch')
class EmployeeEditView(View):
    """
    Employee Edit view. Responsible to show employee edit form. The form has two parts, form_snippet and display_snippet
    Notes:
        - form_snippet and display snippet is defined in schema json file
        - form snippets should be inside jinja2/snippets/<form or display>
    """
    def get(self, request, profile_id=None, errors=None, data=None):
        """
        This will fetch employee edit form
        :return: render page
        """

        if profile_id == request.user.id:
            return redirect('profile_edit')

        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role
        }

        extra_vars = dict()
        extra_vars["errors"] = errors if errors else dict()
        try:

            if profile_id:
                # Trying to edit some others profile
                _employee = models.Employee.get_employee_by_id(profile_id)
            else:
                # Edit by logged user
                _employee = request.user

            context['employee'] = _employee

            # Check authorization
            auth.employee_update(context)

            # if data means some validation errors
            if not data:
                user_data = api_action.get_actions(
                    "show_employee",
                    context,
                    {
                        "id": profile_id or request.user.username
                    }
                )
            else:
                data['id'] = profile_id or request.user.id
                user_data = data
            extra_vars['profile'] = user_data
            extra_vars["schema"] = schemas.get_schema("employee_schema")
            extra_vars["action"] = "edit"
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to see the page")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return render(request, 'profile/edit.html', extra_vars)

    def post(self, request, profile_id=None):
        """
        Edit employee details view. Method=post. ALl form post method should be csrf token.
        :param request: request object
        :param profile_id: str
        :return: redurect to profile/<id> page
        """
        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role,
            "files": request.FILES
        }
        extra_vars = dict()
        is_delete_avatar = True if 'delete_avatar' in request.POST else False
        data_dict = u.convert_request_data_to_dict(request.POST)
        extra_vars['errors'] = dict()
        try:

            if is_delete_avatar:
                context['files'] = {'upload_avatar': ''}

            if profile_id:
                # Trying to edit some others profile
                _employee = models.Employee.get_employee_by_id(profile_id)
            else:
                # Edit by logged user
                _employee = request.user

            # Check authorization
            context['employee'] = _employee
            auth.employee_update(context)

            model_helper.clean_data_dict_for_api_calls(data_dict, params_to_delete=(
                "upload_avatar",
                "delete_avatar"
            ))

            data_dict["id"] = profile_id or request.user.id
            api_action.post_actions(
                "update_employee",
                context,
                data_dict
            )
        except err.ValidationError as e:
            extra_vars['errors'].update(e.args[0])
            u.prepare_error_data(extra_vars['errors'])
            log.error(e)
            messages.error(request, "<br>".join(
                ["{}: {}".format(key, value) for key, value in extra_vars['errors'].items()]
            ))
            if profile_id:
                return self.get(request, profile_id=profile_id, errors=extra_vars['errors'], data=data_dict)
            else:
                return self.get(request, errors=extra_vars['errors'], data=data_dict)
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to edit view")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        if profile_id:
            return redirect('profile', profile_id=profile_id)
        else:
            return redirect('profile')


@method_decorator([login_required], name='dispatch')
class EmployeeCreateView(View):
    """
    Employee create view. Responsible to create employee edit form.
    Form details are same as edit view
    Note:
        - only hr or admin can create a new employee
    """
    def get(self, request, errors=None, data=None):
        """
        View to show user profile. If profile_id=None, then the profile page for logged in user
        :param request: django request object
        :param errors: errors dict if any
        :param data: data dict if any
        :return: render edit page
        """

        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role
        }

        extra_vars = dict()
        extra_vars["errors"] = errors if errors else dict()

        try:
            # check create access
            auth.employee_create(context)
            extra_vars['profile'] = data if data else dict() # if data some validation error
            extra_vars["schema"] = schemas.get_schema("employee_schema")
            extra_vars["action"] = "create"
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to see the page")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return render(request, 'profile/edit.html', extra_vars)

    def post(self, request):
        """
        Create employee details view. Method=post. ALl form post method should be csrf token.
        :param request: request object
        :return: redirect to profile/<id> page
        """
        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role,
            "files": request.FILES
        }
        extra_vars = dict()
        data_dict = u.convert_request_data_to_dict(request.POST)
        extra_vars['errors'] = dict()
        try:
            auth.employee_create(context)
            model_helper.clean_data_dict_for_api_calls(data_dict)
            create_data = api_action.post_actions(
                "create_employee",
                context,
                data_dict
            )
        except err.ValidationError as e:
            extra_vars['errors'].update(e.args[0])
            u.prepare_error_data(extra_vars['errors'])
            log.error(e)
            messages.error(request, "<br>".join(
                ["{}: {}".format(key, value) for key, value in extra_vars['errors'].items()]
            ))
            return self.get(request, errors=extra_vars['errors'], data=data_dict)
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to edit view")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return redirect('profile', profile_id=create_data["id"])


@method_decorator([login_required], name='dispatch')
class EmployeeDeleteView(View):
    """
    This is employee delete view
    """
    def post(self, request, profile_id=None):
        """

        :param request:
        :param profile_id:
        :return:
        """
        if profile_id == request.user.id or not profile_id:
            raise err.ValidationError({
                "profile": "You cannot delete your own profile. Please contact HR or Admin"
            })

        context = {
            "type": "profile",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role
        }

        extra_vars = dict()
        extra_vars['errors'] = dict()
        try:
            auth.employee_create(context)
            api_action.post_actions(
                "delete_employee",
                context,
                {
                    "id": profile_id
                }
            )
        except err.ValidationError as e:
            extra_vars['errors'].update(e.args[0])
            u.prepare_error_data(extra_vars['errors'])
            log.error(e)
            messages.error(request, "<br>".join(
                ["{}: {}".format(key, value) for key, value in extra_vars['errors'].items()]
            ))
            if profile_id:
                return redirect('other_profile', profile_id=profile_id)
            else:
                return redirect('profile')
        except err.NotAuthorizedError:
            messages.error(request, 'You are not authorized to perform this action')
            log.info("Logged in user not authorized to edit view")
            return abort(request, code=401, error_message="You are not authorized to see this page",
                         error_title="Not Authorized")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.", error_title="Not Found")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return redirect('profile_search')
