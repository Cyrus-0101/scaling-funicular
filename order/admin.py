from order.models import Order, OrderItem, ShippingAddress
from django.contrib import admin
from django.contrib.admin.decorators import register

# Register your models here.
admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(ShippingAddress)