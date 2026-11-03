from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_categories(sender, **kwargs):
    """После первой миграции создаёт стартовые категории заявок."""
    from .models import Category

    if not Category.objects.exists():
        for name in ('3D-дизайн', '2D-дизайн', 'Эскиз'):
            Category.objects.get_or_create(name=name)


class StudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studio'
    verbose_name = 'Студия'

    def ready(self):
        post_migrate.connect(create_default_categories, sender=self)
