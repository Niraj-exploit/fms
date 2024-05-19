from django.db.models import Count
from datetime import datetime, timedelta
from .models import Booking, Futsal
from collections import defaultdict
from decimal import Decimal



def find_most_booked_futsal_for_week():
    # Calculate the start and end of the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    print(start_of_week, end_of_week)
    # Query bookings for the current week, annotate with booking count per futsal
    bookings_per_futsal = Booking.objects.filter(
        booking_date__gte=start_of_week,
        booking_date__lte=end_of_week
    ).values('futsal').annotate(num_bookings=Count('id')).order_by('-num_bookings')

    # If there are bookings, get details of the most booked futsal
    if bookings_per_futsal.exists():
        most_booked_futsal_id = bookings_per_futsal[0]['futsal']
        most_booked_futsal = Futsal.objects.get(id=most_booked_futsal_id)
        num_bookings = bookings_per_futsal[0]['num_bookings']
        return most_booked_futsal, num_bookings
    else:
        return None, 0


def calculate_total_money_earned_by_futsals():
    # Initialize a defaultdict to store the total money earned by each futsal
    money_earned_by_futsals = defaultdict(Decimal)
    
    # Query all bookings with payment status 'Completed'
    completed_bookings = Booking.objects.filter(payment_status='Completed')
    
    # Iterate through each completed booking
    for booking in completed_bookings:
        # Add the total price to the corresponding futsal's total money earned
        money_earned_by_futsals[booking.futsal.name] += Decimal(booking.total_price)
    
    return dict(money_earned_by_futsals)