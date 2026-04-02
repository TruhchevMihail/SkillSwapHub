from django.urls import path

from .api_views import BookingCreateAPIView, MyBookingsAPIView

urlpatterns = [
    path('create/<int:offer_pk>/', BookingCreateAPIView.as_view(), name='api-booking-create'),
    path('my/', MyBookingsAPIView.as_view(), name='api-my-bookings'),
]

