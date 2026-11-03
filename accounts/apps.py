from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_admin(sender, **kwargs):
    """После migrate создаёт учётную запись администратора"""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@design.pro',
            password='WSR',
            full_name='Администратор',
        )


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Пользователи'

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)
