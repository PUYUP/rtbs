from rest_framework import serializers
from rtbsapp import models


class BaseTableSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tablenum')
    id = serializers.CharField(source='tablenum')

    class Meta:
        model = models.RestaurantTable
        fields = '__all__'


class BaseBookingSerializer(serializers.ModelSerializer):
    resourceId = serializers.SerializerMethodField()
    title = serializers.CharField(source='fullname')
    start = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='start_time')
    end = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='end_time')

    class Meta:
        model = models.TableBooking
        fields = '__all__'

    def get_resourceId(self, instance):
        if instance.table is not None:
            return instance.table.tablenum
        return None


class BaseTableAvailabilitySerializer(serializers.ModelSerializer):
    tablenum = serializers.CharField(source='table.tablenum')
    tableid = serializers.CharField(source='table.id')

    # Calendar JS expects these fields
    resourceId = serializers.CharField(source='table.tablenum')
    title = serializers.CharField(source='table.tablenum')
    # start = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='start_time')
    # end = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='end_time')

    # Customer information
    customer_initial = serializers.SerializerMethodField()
    booking = BaseBookingSerializer(read_only=True)

    class Meta:
        model = models.TableAvailability
        fields = '__all__'
        read_only_fields = ['is_available']

    def get_customer_initial(self, instance):
        """
        Returns the first letter of the customer's name.
        This is used for displaying initials in the calendar.
        """
        if not instance.booking:
            return None

        if instance.booking.fullname:
            names = instance.booking.fullname.split()
            if len(names) > 1:
                return (names[0][0] + names[-1][0]).upper()
            return names[0][:2].upper()

        return None


"""
Booking Session Serializer
"""


class BaseBookingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookingSession
        fields = '__all__'
        read_only_fields = ['is_active']
