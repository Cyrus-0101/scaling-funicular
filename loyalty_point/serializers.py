# DRF Serializers
from rest_framework import serializers

# Models.
from .models import LoyaltyPoint, LoyaltyPointTransaction

# Serializers.
class LoyaltyPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoint
        fields = '__all__'

class LoyaltyPointTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPointTransaction
        fields = '__all__'

