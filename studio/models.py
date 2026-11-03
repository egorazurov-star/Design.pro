from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .validators import validate_image_extension, validate_image_size


class Category(models.Model):
    """Категория заявок (например, «3D-дизайн», «2D-дизайн», «Эскиз»)."""
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    """Заявка на разработку дизайна интерьера помещения."""
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'Принято в работу'),
        (STATUS_DONE, 'Выполнено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='design_requests', verbose_name='Автор',
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    # При удалении категории удаляются все её заявки (требование задания)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='requests', verbose_name='Категория',
    )
    photo = models.ImageField(
        'Фото помещения или план', upload_to='requests/%Y/%m/',
        validators=[validate_image_extension, validate_image_size],
        help_text='Форматы: jpg, jpeg, png, bmp. Размер не более 2 МБ.',
    )
    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW,
    )
    comment = models.TextField('Комментарий', blank=True)
    design_image = models.ImageField(
        'Изображение дизайна', upload_to='designs/%Y/%m/', blank=True,
        validators=[validate_image_extension, validate_image_size],
        help_text='Форматы: jpg, jpeg, png, bmp. Размер не более 2 МБ.',
    )
    # Временная метка создаётся автоматически при добавлении заявки
    created_at = models.DateTimeField('Дата и время', auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return self.title


@receiver(post_delete, sender=DesignRequest)
def delete_request_files(sender, instance, **kwargs):
    """Удаляет файлы изображений вместе с заявкой."""
    for image in (instance.photo, instance.design_image):
        if image:
            image.delete(save=False)
