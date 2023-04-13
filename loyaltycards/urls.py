from django.urls import path, include
from rest_framework import routers
from .views import CustomerViewSet, RedemptionViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('customers', CustomerViewSet)
router.register('redemptions', RedemptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
