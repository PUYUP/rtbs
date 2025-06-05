from django import forms


class ConstanteForm(forms.Form):
    background_image = forms.ImageField()
    background_color_booking_form = forms.CharField()
