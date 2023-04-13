from django.urls import path
from .views import redeem, point_balance, redemption_history, authorize_redemption

urlpatterns = [
    path('redeem/',
