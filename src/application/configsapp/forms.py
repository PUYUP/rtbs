from django import forms


class ConstanteForm(forms.Form):
    background_image = forms.ImageField(widget=forms.FileInput())
    background_color_booking_form = forms.CharField()
