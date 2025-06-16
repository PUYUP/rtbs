from rest_framework import serializers
from rtbsapp.models import Resturanttable, Tablebooking


class BaseTableSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tablenum')
    id = serializers.CharField(source='tablenum')

    class Meta:
        model = Resturanttable
        fields = '__all__'


class BaseBookingSerializer(serializers.ModelSerializer):
    resourceId = serializers.SerializerMethodField()
    title = serializers.CharField(source='fullname')
    start = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='start_time')
    end = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", source='end_time')

    class Meta:
        model = Tablebooking
        fields = '__all__'

    def get_resourceId(self, instance):
        if instance.table_id is not None:
            return instance.table_id.tablenum
        return None
