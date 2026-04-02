from django.utils import timezone
from rest_framework import serializers

from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('preferred_date', 'message')

    def validate_preferred_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Preferred date must be in the future.')
        return value

    def validate(self, attrs):
        offer = self.context['offer']
        user = self.context['request'].user

        if offer.owner == user:
            raise serializers.ValidationError('You cannot book your own offer.')

        if not offer.is_active:
            raise serializers.ValidationError('Inactive offers cannot be booked.')

        return attrs

    def create(self, validated_data):
        offer = self.context['offer']
        user = self.context['request'].user

        return Booking.objects.create(
            offer=offer,
            learner=user,
            status=Booking.Status.PENDING,
            **validated_data,
        )


class BookingListSerializer(serializers.ModelSerializer):
    offer = serializers.CharField(source='offer.title', read_only=True)
    mentor = serializers.CharField(source='offer.owner.username', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'offer',
            'mentor',
            'preferred_date',
            'message',
            'status',
            'created_at',
        )

