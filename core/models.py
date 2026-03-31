from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityLog(models.Model):
    ACTION_OFFER_CREATED = 'offer_created'
    ACTION_OFFER_UPDATED = 'offer_updated'
    ACTION_OFFER_DELETED = 'offer_deleted'
    ACTION_BOOKING_CREATED = 'booking_created'
    ACTION_BOOKING_STATUS_CHANGED = 'booking_status_changed'
    ACTION_BOOKING_CANCELLED = 'booking_cancelled'
    ACTION_REVIEW_CREATED = 'review_created'
    ACTION_REVIEW_UPDATED = 'review_updated'
    ACTION_REVIEW_DELETED = 'review_deleted'

    ACTION_CHOICES = (
        (ACTION_OFFER_CREATED, 'Offer created'),
        (ACTION_OFFER_UPDATED, 'Offer updated'),
        (ACTION_OFFER_DELETED, 'Offer deleted'),
        (ACTION_BOOKING_CREATED, 'Booking created'),
        (ACTION_BOOKING_STATUS_CHANGED, 'Booking status changed'),
        (ACTION_BOOKING_CANCELLED, 'Booking cancelled'),
        (ACTION_REVIEW_CREATED, 'Review created'),
        (ACTION_REVIEW_UPDATED, 'Review updated'),
        (ACTION_REVIEW_DELETED, 'Review deleted'),
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs',
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey('content_type', 'object_id')

    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        actor_name = self.actor.username if self.actor else 'system'
        return f'{actor_name}: {self.action}'

