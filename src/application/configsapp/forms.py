from django import forms


class ConstanteForm(forms.Form):
    background_image = forms.ImageField(required=False)
    background_color_booking_form = forms.CharField(required=False)
