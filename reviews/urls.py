from django.urls import path

from .views import ReviewCreateView, ReviewDeleteView, ReviewUpdateView

urlpatterns = [
    path('create/<int:booking_pk>/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]

