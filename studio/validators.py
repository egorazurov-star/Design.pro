from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp']
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 МБ

validate_image_extension = FileExtensionValidator(
    allowed_extensions=ALLOWED_EXTENSIONS,
    message='Допустимые форматы изображения: jpg, jpeg, png, bmp.',
)


def validate_image_size(file):
    """Размер изображения не должен превышать 2 МБ."""
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError('Размер файла не должен превышать 2 МБ.')
