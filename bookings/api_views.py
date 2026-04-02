from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from offers.models import SkillOffer

from .models import Booking
from .serializers import BookingCreateSerializer, BookingListSerializer


class BookingCreateAPIView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['offer'] = get_object_or_404(SkillOffer, pk=self.kwargs['offer_pk'])
        return context


class MyBookingsAPIView(ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(learner=self.request.user).select_related('offer', 'offer__owner')

