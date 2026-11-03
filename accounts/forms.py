from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


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


class RegistrationForm(forms.Form):
    """Форма регистрации. Вся валидация выполняется на стороне сервера."""
    full_name = forms.CharField(
        label='ФИО',
        max_length=150,
        validators=[RegexValidator(
            r'^[А-Яа-яЁё\s-]+$',
            'ФИО может содержать только кириллические буквы, дефис и пробелы.',
        )],
        help_text='Только кириллические буквы, дефис и пробелы.',
    )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        validators=[RegexValidator(
            r'^[A-Za-z-]+$',
            'Логин может содержать только латинские буквы и дефис.',
        )],
        help_text='Только латинские буквы и дефис.',
    )
    email = forms.EmailField(label='Email', max_length=254)
    password1 = forms.CharField(
        label='Пароль', strip=False, widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Повтор пароля', strip=False, widget=forms.PasswordInput,
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        error_messages={'required': 'Необходимо дать согласие на обработку персональных данных.'},
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')
        return cleaned

    def save(self):
        """Создаёт пользователя; пароль сохраняется в виде хеша."""
        data = self.cleaned_data
        return get_user_model().objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
            full_name=data['full_name'],
        )
