from django.db.models.signals import post_save, pre_save

# User Model.
from .models import User

# Loyalty Point Model.
from loyalty_point.models import LoyaltyPoint

def create_loyalty_point(sender, created, instance, **kwargs):
    if created:
        LoyaltyPoint.objects.create(user=instance)

post_save.connect(create_loyalty_point, sender=User)
