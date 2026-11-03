from django import forms

from .models import DesignRequest


class DesignRequestForm(forms.ModelForm):
    """Создание заявки. Все поля обязательны; изображение проверяется на формат и размер."""

    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'photo': forms.ClearableFileInput(
                attrs={'accept': 'image/jpeg,image/png,image/bmp'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '— выберите категорию —'


class InProgressForm(forms.ModelForm):
    """Перевод заявки в статус «Принято в работу» - комментарий обязателен."""
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = DesignRequest
        fields = ['comment']


class DoneForm(forms.ModelForm):
    """Перевод заявки в статус «Выполнено» - изображение дизайна обязательно."""
    design_image = forms.ImageField(
        label='Изображение дизайна',
        help_text='Форматы: jpg, jpeg, png, bmp. Размер не более 2 МБ.',
        widget=forms.ClearableFileInput(
            attrs={'accept': 'image/jpeg,image/png,image/bmp'}
        ),
    )

    class Meta:
        model = DesignRequest
        fields = ['design_image']
