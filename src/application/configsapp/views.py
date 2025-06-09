import json
import os
import mimetypes

from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_sameorigin
from constance.management.commands import constance
from constance.models import Constance
from constance import config, settings as constance_settings, base
from . import forms


class WebpageSettingsView(View):
    template_name = 'webpage-settings-page.html'
    context = {}

    def get(self, request):
        set_for_value = {}
        base_config = base.Config()
        for k in constance_settings.CONFIG.keys():
            set_for_value.update({k.lower(): base_config.__getattr__(k)})

        form = forms.ConstanteForm(initial={**set_for_value})
        self.context.update({'form': form})
        return render(request, self.template_name, context=self.context)

    @transaction.atomic()
    def post(self, request):
        form = forms.ConstanteForm(request.POST, request.FILES)
        self.context.update({'form': form})
        if form.is_valid():
            for field in form:
                key = field.name.upper()
                value = form.cleaned_data.get(field.name, None)
                if value:
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


class ManuPageView(View):
    template_name = 'manu-page.html'
    context = {}

    @xframe_options_sameorigin
    def get(self, request):
        file_content = config.MANU_PAGE_CONTENT
        self.context.update({
            'mime_type': self.get_mime_type(file_content),
            'file_url': request.build_absolute_uri(settings.MEDIA_URL + file_content),
        })
        return render(request, self.template_name, self.context)

    def get_mime_type(self, filename):
        """Guesses the MIME type of a file based on its extension."""
        mime_type, encoding = mimetypes.guess_type(filename)
        return mime_type
