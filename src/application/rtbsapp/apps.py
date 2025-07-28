from django.apps import AppConfig
from django.db.models.signals import post_save


class RtbsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rtbsapp'

    def ready(self):
        from rtbsapp.models import TableBooking
        from rtbsapp.signals import table_booking_save_handler

        post_save.connect(
            table_booking_save_handler,
            sender=TableBooking,
            dispatch_uid='table_booking_save_handler'
        )
