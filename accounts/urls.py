from django.urls import path
from .views import RegisterUserView, SignInView, SignOutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
]
