from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import SkillOffer
from .serializers import OfferDetailSerializer, OfferListSerializer


class OfferListAPIView(ListAPIView):
    serializer_class = OfferListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            SkillOffer.objects.filter(is_active=True)
            .select_related('owner', 'category')
            .prefetch_related('tags')
        )


class OfferDetailAPIView(RetrieveAPIView):
    serializer_class = OfferDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            SkillOffer.objects.filter(is_active=True)
            .select_related('owner', 'category')
            .prefetch_related('tags')
        )

