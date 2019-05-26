"""Garage endpoints."""
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path


urlpatterns = [
    path('garage/auth/login', obtain_auth_token, name='api_token_auth')
]
