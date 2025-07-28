from django.urls import path
from .v1 import views


urlpatterns = [
    path('v1/tables/', views.TableListView.as_view(), name='tables'),
    path('v1/bookings/', views.BookingListView.as_view(), name='bookings'),
    path(
        'v1/availabilities/',
        views.TableAvailabilityView.as_view(),
        name='table_availabilities'
    ),
]
