
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rtbsapp import urls as rtbsapp_urls
from configsapp import urls as configsapp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(rtbsapp_urls)),
    path('', include(configsapp_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
