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
