from django import forms
from django.forms import widgets
from rtbsapp.models import TimeSlot


class TimeSlotForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        required=False,
        widget=widgets.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    end_datetime = forms.DateTimeField(
        required=False,
        widget=widgets.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = TimeSlot
        fields = '__all__'
