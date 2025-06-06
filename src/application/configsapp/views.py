import json
from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from constance.management.commands import constance
from constance.models import Constance
from constance import config
from . import forms


class WebpageSettingsView(View):
    template_name = 'webpage-settings-page.html'
    context = {}

    def get(self, request):
        form = forms.ConstanteForm(initial={
            'background_color_booking_form': config.BACKGROUND_COLOR_BOOKING_FORM,
            'background_image': config.BACKGROUND_IMAGE,
        })
        self.context.update({'form': form})
        return render(request, self.template_name, context=self.context)

    @transaction.atomic()
    def post(self, request):
        form = forms.ConstanteForm(request.POST, request.FILES)
        self.context.update({'form': form})
        if form.is_valid():
            for field in form:
                key = field.name.upper()
                value = form.cleaned_data.get(field.name, '')
                if isinstance(value, InMemoryUploadedFile):
                    fs = FileSystemStorage()
                    filename = fs.save(value.name, value)
                    defaults = {
                        "__type__": "default",
                        "__value__": filename,
                    }
                    Constance.objects.update_or_create(
                        key=key,
                        defaults={'value': json.dumps(defaults)})
                else:
                    constance._set_constance_value(key, value)
            messages.success(request, "Your webpage settings successfully changed.")
            return redirect('webpage_settings')
        return render(request, self.template_name, context=self.context)
