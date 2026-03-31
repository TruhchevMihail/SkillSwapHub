from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from bookings.models import Booking


class Review(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='written_reviews',
    )

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.rating and (self.rating < 1 or self.rating > 5):
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

        if self.booking_id:
            if self.booking.status != Booking.Status.COMPLETED:
                raise ValidationError('You can only review completed bookings.')

            if self.author_id != self.booking.learner_id:
                raise ValidationError('Only the learner from the booking can write a review.')

            if self.mentor_id != self.booking.offer.owner_id:
                raise ValidationError('The mentor must match the owner of the booked offer.')

    def __str__(self):
        return f'Review by {self.author.username} for {self.mentor.username} ({self.rating}/5)'

    def get_absolute_url(self):
        return reverse('offer-detail', kwargs={'pk': self.booking.offer.pk})

