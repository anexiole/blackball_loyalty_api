from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=50)

class LoyaltyPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
