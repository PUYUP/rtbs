from django.urls import path
from .views import TableListView, BookingListView


urlpatterns = [
    path('tables/', TableListView.as_view(), name='tables'),
    path('bookings/', BookingListView.as_view(), name='bookings'),
]
