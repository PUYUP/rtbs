from rest_framework import generics
from rtbsapp.models import Resturanttable, Tablebooking
from rtbsapp.api.serializers import BaseTableSerializer, BaseBookingSerializer


class TableListView(generics.ListAPIView):
    queryset = Resturanttable.objects.all()
    serializer_class = BaseTableSerializer


class BookingListView(generics.ListAPIView):
    queryset = Tablebooking.objects.all()
    serializer_class = BaseBookingSerializer
