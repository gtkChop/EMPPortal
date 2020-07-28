from django.contrib.auth import views as auth_views
from django.contrib import messages
import logging

log = logging.getLogger(__name__)


class EMAppLoginView(auth_views.LoginView):
    pass


class EMAppLogoutView(auth_views.LogoutView):

    def get(self, request, *args, **kwargs):
        """
        Add a logout message as notification
        :return:
        """
        messages.success(request, 'You are logged out successfully.')
        return super(self.__class__, self).get(request, *args, **kwargs)


class EMAppPasswordResetView(auth_views.PasswordResetView):
    pass


class EMAppPasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass


class EMAppPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass


class EMAppPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass


class EMAppPasswordChangeView(auth_views.PasswordChangeView):
    pass
