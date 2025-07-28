from django.contrib import admin
from rtbsapp import models

admin.site.register(models.RestaurantTable)
admin.site.register(models.TableBooking)
admin.site.register(models.BookingSession)


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_filter = ('day_of_week', 'session', 'is_available')
    list_display = (
        'session',
        'start_time',
        'end_time',
        'day_of_week',
        'is_available'
    )


@admin.register(models.TableAvailability)
class TableAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'table',
        'timeslot',
        'day_of_week',
        'start_time',
        'end_time',
        'is_available'
    )
    list_filter = ('table', 'availability_date', 'is_available')
    search_fields = ('table__tablenum',)
    ordering = ('-availability_date', 'start_time')
    raw_id_fields = ('table', 'timeslot')

    def get_queryset(self, request):
        """
        Override to prefetch related objects for better performance.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('table', 'timeslot')
