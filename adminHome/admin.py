from django.contrib import admin
from .models import Booking, Futsal


admin.site.register(Futsal)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'futsal', 'booking_date', 'get_booking_time', 'get_status_display')

    def get_booking_time(self, obj):
        return obj.booking_time.strftime("%I:%M %p") if obj.booking_time else None

    get_booking_time.short_description = 'Booking Time'
