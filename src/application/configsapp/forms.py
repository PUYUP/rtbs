from django import forms
from constance import settings


class ConstanteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k in settings.CONFIG:
            obj = settings.CONFIG.get(k)
            lower_k = k.lower()
            typi = obj[2]

            # Default is text field
            self.fields[lower_k] = forms.CharField(required=False)

            # Replace with matching field
            if typi == 'file_field':
                self.fields[lower_k] = forms.FileField(required=False)

            if typi == 'image_field':
                self.fields[lower_k] = forms.ImageField(required=False)
