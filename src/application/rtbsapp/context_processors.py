from .models import TableBooking


def booking_processor(request):
    booking_details = TableBooking.objects.filter(status='pending')
    booking_status = TableBooking.objects.filter(status='pending').count()
    return {
        'booking_status': booking_status,
        'booking_details': booking_details,
    }
