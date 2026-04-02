from django.urls import path

from .api_views import OfferDetailAPIView, OfferListAPIView

urlpatterns = [
    path('', OfferListAPIView.as_view(), name='api-offer-list'),
    path('<int:pk>/', OfferDetailAPIView.as_view(), name='api-offer-detail'),
]

