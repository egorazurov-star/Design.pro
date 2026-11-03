from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, resolve_url

from .forms import LoginForm, RegistrationForm


class UserLoginView(LoginView):
    """Страница входа. Администратор попадает в панель управления, остальные - в личный кабинет."""
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        if self.request.user.is_staff:
            return resolve_url('superadmin')
        return resolve_url('cabinet')


def register(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        return redirect('cabinet')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти.')
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})
