from .models import Tablebooking

def booking_processor(request):
    booking_details = Tablebooking.objects.filter(status='pending')
    booking_status = Tablebooking.objects.filter(status='pending').count()
    return {'booking_status': booking_status,
    'booking_details':booking_details,}