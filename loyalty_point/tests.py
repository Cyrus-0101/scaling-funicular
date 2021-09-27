# Unit Test
from django.test import TestCase

# User Model
from django.contrib.auth import get_user_model

# Models.
from loyalty_point.models import LoyaltyPoint, LoyaltyPointTransaction

# Create your tests here.

# LoyaltyPoint Tests.
class LoyaltyPointTests(TestCase):
    """
        Test to create new LoyaltyPoint.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        loyal = LoyaltyPoint.objects.create(
            user=super_user,
            totalPoints=0,
        )

        # When a user is created we have a signal that automtically creates 
        # Loyalty Point Model, we never have to write that code.

    def test_new_loyalty_point(self):
        loyaltyPoint = LoyaltyPoint.objects.get(user=1)

        self.assertEqual(str(loyaltyPoint), loyaltyPoint.user.username)

# Loyalty Point Transaction Tests.
class LoyaltyPointTransactionTests(TestCase):
    """
        Test to create new Loyalty Point Transaction.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        # When a user is created we have a signal that automtically creates 
        # Loyalty Point Model, we never have to write that code.

        loyal = LoyaltyPoint.objects.create(
            user=super_user,
            totalPoints=0,
        )

        LoyaltyPointTransaction.objects.create(
            loyaltyPoint=loyal,
            transactionPoints=10.00,
            transactionType="accrew",
            transactionPrice=1800.00,
            redeemedAt=None,
        )

    def test_new_loyalty_point_transaction(self):
        loyaltyPoint = LoyaltyPointTransaction.objects.get(id=1)

        self.assertEqual(str(loyaltyPoint), loyaltyPoint.transactionType)
