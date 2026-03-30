from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'offer',
        'learner',
        'preferred_date',
        'status',
        'created_at',
    )
    list_filter = ('status', 'preferred_date')
    search_fields = (
        'offer__title',
        'learner__username',
        'message',
    )

