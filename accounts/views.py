from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url

from .forms import LoginForm


class UserLoginView(LoginView):
    """Страница входа. Администратор попадает в панель управления, остальные - в личный кабинет."""
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        if self.request.user.is_staff:
            return resolve_url('superadmin')
        return resolve_url('cabinet')
