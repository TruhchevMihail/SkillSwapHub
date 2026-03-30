from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from offers.models import SkillOffer


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'
        CANCELLED = 'Cancelled', 'Cancelled'
        COMPLETED = 'Completed', 'Completed'

    offer = models.ForeignKey(
        SkillOffer,
        on_delete=models.CASCADE,
        related_name='bookings',
    )

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )

    preferred_date = models.DateTimeField()

    message = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        from django.utils import timezone

        if self.preferred_date and self.preferred_date <= timezone.now():
            raise ValidationError({
                'preferred_date': 'Preferred date must be in the future.'
            })

        if self.offer_id and self.learner_id and self.offer.owner_id == self.learner_id:
            raise ValidationError('You cannot book your own offer.')

        if self.offer_id and not self.offer.is_active:
            raise ValidationError('Inactive offers cannot be booked.')

    def __str__(self):
        return f'{self.learner.username} -> {self.offer.title} ({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})
