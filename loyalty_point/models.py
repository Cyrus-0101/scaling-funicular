# Model Abstraction.
from django.db import models

# User Model.
from authentication.models import User

# Create your models here.
# Loyalty Points
class LoyaltyPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    totalPoints = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user.username)

# Loyalty Points Transaction
class LoyaltyPointTransaction(models.Model):
    TRANSACTION_TYPE_OPTIONS = [
        ('accrew', 'Accrew'),
        ('redeem', 'Redeem'),
    ]

    TRANSACTION_RESTAURANT_OPTIONS = [
        ('mbuzi munch lavington', 'Mbuzi Munch Lavington'),
        ('mbuzi munch naivasha', 'Mbuzi Munch Naivasha'),
        ('mbuzi munch galleria', 'Mbuzi Munch Galleria')

    ]
    loyaltyPoint = models.ForeignKey(LoyaltyPoint, on_delete=models.CASCADE)
    transactionPoints = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    transactionType = models.CharField(choices=TRANSACTION_TYPE_OPTIONS, max_length=50)
    transactionRestaurant=models.CharField(choices=TRANSACTION_RESTAURANT_OPTIONS, max_length=50)
    transactionPrice = models.DecimalField(max_digits=7, decimal_places=2)
    redeemedAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    REQUIRED_FIELDS = ['loyaltyPoint', 'transactionType', 'transactionRestaurant', 'transactionPrice']
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.transactionType)
