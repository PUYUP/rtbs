from django.contrib import admin
from rtbsapp.models import Tablebooking, Resturanttable, TimeSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('label', 'enabled', 'typeof', 'increment_value',
                    'start_datetime', 'end_datetime', )


admin.site.register(Resturanttable)
admin.site.register(Tablebooking)
admin.site.register(TimeSlot, TimeSlotAdmin)
