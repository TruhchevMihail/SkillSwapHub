from django.urls import path

from .views import (
    FavoriteOffersListView,
    MyOffersListView,
    OfferCreateView,
    OfferDeleteView,
    OfferDetailView,
    OfferListView,
    OfferUpdateView,
    ToggleFavoriteView,
)

urlpatterns = [
    path('', OfferListView.as_view(), name='offer-list'),
    path('create/', OfferCreateView.as_view(), name='offer-create'),
    path('my-offers/', MyOffersListView.as_view(), name='my-offers'),
    path('favorites/', FavoriteOffersListView.as_view(), name='favorite-offers'),
    path('<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('<int:pk>/edit/', OfferUpdateView.as_view(), name='offer-edit'),
    path('<int:pk>/delete/', OfferDeleteView.as_view(), name='offer-delete'),
    path('<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='toggle-favorite'),
]
