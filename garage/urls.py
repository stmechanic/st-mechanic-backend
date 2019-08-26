"""Garage endpoints."""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_swagger.views import get_swagger_view

from .views import GarageCreateViewSet, VehicleViewSet

schema_view = get_swagger_view(title='Garage API')


urlpatterns = [
    path('garage/api/auth/register', GarageCreateViewSet.as_view({'post': 'create'})),
    path('garage/api/auth/login',  TokenObtainPairView.as_view(), name='api_token_auth'),
    path('garage/api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('garage/api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('garage/api/vehicles', VehicleViewSet.as_view({
        'post': 'create', 'get': 'list'})),
    path('garage/api/docs', schema_view)

]
