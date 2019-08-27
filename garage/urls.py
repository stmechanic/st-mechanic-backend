"""Garage endpoints."""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from .views import GarageCreateViewSet, VehicleViewSet, MechanicViewSet, RatingViewSet, QuoteViewSet, JobViewSet, \
    PaymentViewSet

router = routers.DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'mechanics', MechanicViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'quotes', QuoteViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'payments', PaymentViewSet)

schema_view = get_swagger_view(title='Garage API')

urlpatterns = [
    path('garage/api/', include(router.urls)),
    path('garage/admin/', admin.site.urls),
    path('garage/admin/docs/', include('django.contrib.admindocs.urls')),
    path('garage/api/auth/register', GarageCreateViewSet.as_view({'post': 'create'})),
    path('garage/api/auth/login',  TokenObtainPairView.as_view(), name='api_token_auth'),
    path('garage/api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('garage/api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('garage/api/docs', schema_view),
]
