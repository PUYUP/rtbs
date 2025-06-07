from django.urls import path
from . import views

urlpatterns = [
    path('webpage-settings/',
         views.WebpageSettingsView.as_view(),
         name='webpage_settings'),
    path('manu/', views.ManuPageView.as_view(), name='manu-page'),
]
