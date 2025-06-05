from django.shortcuts import render
from django.views import View
from django.db import transaction
from constance.management.commands import constance
from . import forms


class WebpageSettingsView(View):
    template_name = 'webpage-settings-page.html'
    context = {}

    def get(self, request):
        form = forms.ConstanteForm()
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
                constance._set_constance_value(key, value)
        return render(request, self.template_name, context=self.context)
