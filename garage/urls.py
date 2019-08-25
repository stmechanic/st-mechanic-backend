"""Garage endpoints."""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import GarageCreateViewSet


urlpatterns = [
    path('garage/auth/register', GarageCreateViewSet.as_view({'post': 'create'})),
    path('garage/auth/login',  TokenObtainPairView.as_view(), name='api_token_auth'),
    path('garage/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('garage/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
