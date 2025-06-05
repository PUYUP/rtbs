from django.urls import path
from . import views

urlpatterns = [
    path('webpage-settings/',
         views.WebpageSettingsView.as_view(),
         name='webpage-settings')
]
