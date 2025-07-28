from django.db import transaction


@transaction.atomic()
def table_booking_save_handler(sender, instance, created, **kwargs):
    """
    Signal that's triggered after TableBooking instance is saved
    """
    if instance.status == 'confirmed':
        # Perform actions when a booking is confirmed
        print(f"Booking {instance.id} has been confirmed.")
        instance.mark_timeslot_unavailable()
    elif instance.status == 'cancelled':
        # Perform actions when a booking is cancelled
        print(f"Booking {instance.id} has been cancelled.")
        instance.mark_timeslot_available()
