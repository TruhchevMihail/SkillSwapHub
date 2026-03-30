from django.urls import path

from .views import (
    BookingCancelView,
    BookingCreateView,
    BookingDetailView,
    BookingStatusUpdateView,
    MentorBookingsListView,
    MyBookingsListView,
)

urlpatterns = [
    path('create/<int:offer_pk>/', BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', MyBookingsListView.as_view(), name='my-bookings'),
    path('mentor-bookings/', MentorBookingsListView.as_view(), name='mentor-bookings'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/status/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]

