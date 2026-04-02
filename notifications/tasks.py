from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from bookings.models import Booking


@shared_task
def send_booking_reminder(booking_id):
    try:
        booking = Booking.objects.select_related('offer', 'learner', 'offer__owner').get(pk=booking_id)
    except Booking.DoesNotExist:
        return 'Booking does not exist.'

    message = (
        f'Reminder: Booking for "{booking.offer.title}" '
        f'between {booking.learner.username} and {booking.offer.owner.username} '
        f'is scheduled for {booking.preferred_date}.'
    )

    print(message)
    return message


@shared_task
def send_review_reminder(booking_id):
    try:
        booking = Booking.objects.select_related('offer', 'learner', 'offer__owner').get(pk=booking_id)
    except Booking.DoesNotExist:
        return 'Booking does not exist.'

    message = (
        f'Review reminder: {booking.learner.username} can now leave a review '
        f'for "{booking.offer.title}".'
    )

    print(message)
    return message


@shared_task
def cleanup_stale_pending_bookings():
    cutoff = timezone.now() - timedelta(days=2)

    stale_bookings = Booking.objects.filter(
        status=Booking.Status.PENDING,
        created_at__lt=cutoff,
    )

    count = stale_bookings.update(status=Booking.Status.CANCELLED)

    message = f'{count} stale pending bookings were cancelled.'
    print(message)
    return message

