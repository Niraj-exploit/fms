from django.utils import timezone
from adminHome.models import Booking

def find_nearest_booking():
    current_time = timezone.now()
    nearest_booking = Booking.objects.filter(
        booking_date__gte=current_time.date(),
        booking_time__gte=current_time.time(),
        status='Approved'
    ).order_by('booking_date', 'booking_time').first()
    return nearest_booking
