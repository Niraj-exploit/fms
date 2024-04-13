from django.contrib import admin
from .models import Futsal, Booking

admin.site.register(Futsal)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'futsal', 'booking_date', 'booking_time', 'book_time', 'get_status_display')

