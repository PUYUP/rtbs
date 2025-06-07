from django import forms


class ConstanteForm(forms.Form):
    tagline = forms.CharField(required=False)
    background_image = forms.ImageField(required=False)
    logo_image = forms.ImageField(required=False)
    background_color_booking_form = forms.CharField(required=False)
    manu_page_content = forms.FileField(required=False)
