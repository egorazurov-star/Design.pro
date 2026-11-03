from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Форма входа: при неверной паре логин-пароль выводится сообщение об ошибке."""
    error_messages = {
        'invalid_login': 'Неверный логин или пароль.',
        'inactive': 'Эта учётная запись отключена.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
