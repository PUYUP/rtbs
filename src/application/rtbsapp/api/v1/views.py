from rest_framework import generics
from rtbsapp import models
from .serializers import (
    BaseTableSerializer,
    BaseBookingSerializer,
    BaseTableAvailabilitySerializer,
    BaseBookingSessionSerializer,
)


class TableListView(generics.ListAPIView):
    queryset = models.RestaurantTable.objects.all()
    serializer_class = BaseTableSerializer


class BookingListView(generics.ListAPIView):
    queryset = models.TableBooking.objects.all()
    serializer_class = BaseBookingSerializer


class TableAvailabilityView(generics.ListAPIView):
    """
    This view can be used to check the availability of tables.
    It can be extended to filter by date, time, or other criteria.
    """
    queryset = models.TableAvailability.objects.all()
    serializer_class = BaseTableAvailabilitySerializer

    def get_queryset(self):
        """
        Optionally filter the queryset based on query parameters.
        For example, you could filter by date or time if needed.
        """
        day_of_week = self.request.query_params.get('day_of_week')
        queryset = super().get_queryset() \
            .prefetch_related('table', 'timeslot', 'booking')
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)
        return queryset


"""
Booking Session View
This view can be used to manage booking sessions.
"""


class BookingSessionListCreateView(generics.ListCreateAPIView):
    queryset = models.BookingSession.objects.all()
    serializer_class = BaseBookingSessionSerializer

    def get_queryset(self):
        """
        Optionally filter the queryset based on query parameters.
        For example, you could filter by session date or status.
        """
        queryset = super().get_queryset()
        return queryset
