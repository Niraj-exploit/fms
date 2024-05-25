from django.utils import timezone
from adminHome.models import Booking

def find_nearest_booking(user):
    nearest_booking = Booking.objects.filter(user=user, status='Approved').order_by('booking_date', 'booking_time').first()
    return nearest_booking
