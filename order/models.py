# Phone Number Field.
from phonenumber_field.modelfields import PhoneNumberField

# User Model.
from authentication.models import User

# Product Model.
from product.models import Product

# Models Abstraction.
from django.db import models

# Create your models here.

# Order Model
class Order(models.Model):
    PAYMENT_METHOD_OPTIONS = [
        ('mpesa', 'Mpesa'),
        ('equity', 'Equity'),
        ('payPal', 'PayPal'),
        ('cash', 'Cash'),
        ('redeemPoints', 'RedeemPoints')
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(choices=PAYMENT_METHOD_OPTIONS, max_length=50, null=True, blank=True)
    vatPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    digitalservicetaxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['createdAt']

    def __str__(self):
        return str(self.user.username)

# OrderItem Model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.name)

# Shipping Address Model
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postalCode = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    phoneNumber = PhoneNumberField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['_id']

    def __str__(self):
        return str(self.address)