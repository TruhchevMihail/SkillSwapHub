from django.urls import path
from .views import (
    ProfileDetailView,
    ProfileEditView,
    ProfilePasswordChangeView,
    RegisterUserView,
    SignInView,
    SignOutView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/password/', ProfilePasswordChangeView.as_view(), name='password-change'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile-detail'),
]
