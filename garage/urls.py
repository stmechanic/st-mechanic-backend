"""Garage endpoints."""
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('garage/auth/login', obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
