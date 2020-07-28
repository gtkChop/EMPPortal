from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from emappcore.utils import errors as err
from emappcore.common import abort, server_error, schemas, utilities
from emappext.hr_mgmt.logic.employee import _search_employee_for_pagination as search_employee_object
import logging

log = logging.getLogger(__name__)


@method_decorator([login_required], name='dispatch')
class EmployeeSearch(View):
    """
    View class for profile/Employee search. Employee search is paginated and data is fetched from index see
    the api logic function search_employee_object and to see what are the fields that are indexed.
    User can search following fields:
        - employee id
        - first name
        - middle name
        - last name
        - email id
        - position
    """

    _items_per_page = 12

    def get(self, request):
        """
        see the api search_employee_object for query fields and details
        :param request: django request object
        :return: render search results
        """
        data_dict = dict()
        for _key in request.GET:
            data_dict[_key] = request.GET[_key]

        page = data_dict.get('page', 1)

        context = {
            "type": "search",
            "user": request.user,
            "is_superuser": request.user.is_superuser,
            "role": request.user.role
        }
        extra_vars = dict()

        try:
            search_result = search_employee_object(context, data_dict)
            paginator = Paginator(search_result, self._items_per_page)

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            extra_vars['total_pages'] = paginator.num_pages
            extra_vars['q'] = data_dict.get('q')
            extra_vars['search_results'] = results
            extra_vars['profile'] = request.user
            extra_vars['result_count'] = search_result.count()
            extra_vars['employee_count'] = utilities.get_total_employee_count()

        except err.NotAuthorizedError:
            log.info("Logged in user not authorized to see the page")
            return abort(request, code=401, error_message="You are not authorized to see this page")
        except (err.UserNotFound, err.NotFoundError) as e:
            log.info(e)
            return abort(request, code=404, error_message="User Not found.")
        except Exception as e:
            log.error(e)
            return server_error(request, code=500, error_message="Server Error. Something wrong")

        return render(request, 'profile/search.html', extra_vars)

