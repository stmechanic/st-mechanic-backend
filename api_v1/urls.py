from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import (BankingUserCreateViewSet, BankingUserVerifyViewSet,
                    BankAccountViewSet, TransactionViewSet)

router = routers.SimpleRouter()
router.register('account', BankAccountViewSet)

urlpatterns = [
    path(
        'auth/register/',
        BankingUserCreateViewSet.as_view({'post': 'create'}),
        name='user-register'
    ),
    path(
        'auth/verify/',
        BankingUserVerifyViewSet.as_view({'post': 'verify'}),
        name='user-verify'
    ),
    path('auth/login/', obtain_jwt_token, name='user-verify'),
    path('accounts/', BankAccountViewSet.as_view({
        'post': 'create',
        'get': 'list'})),
]
