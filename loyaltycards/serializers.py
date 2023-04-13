from rest_framework import serializers
from .models import Customer, Redemption

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = '__all__'
