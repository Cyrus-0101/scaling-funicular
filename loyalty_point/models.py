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
    loyaltyPoint = models.ForeignKey(LoyaltyPoint, on_delete=models.CASCADE)
    transactionPoints = models.DecimalField(max_digits=5, decimal_places=2)
    transactionType = models.CharField(choices=TRANSACTION_TYPE_OPTIONS, max_length=50)
    transactionPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    redeemedAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['_id']

    def __str__(self):
        return str(self.transactionType)
