# Unit Test
from django.test import TestCase

# User Model
from django.contrib.auth import get_user_model

# Create your tests here.
class UserAccountTests(TestCase):
    """
        Test to create new super user.
    """
    def test_new_superuser(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password

        )

        self.assertEqual(super_user.email, 'test@superuser.com')
        self.assertEqual(super_user.username, 'Username')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_verified)

        # Checks to see if super user object returns an email string as per model.
        self.assertEqual(str(super_user), 'test@superuser.com')

        # Testing our ValueError cases Custom AccountManager.
        # Testing whether a superuser can be created and be False.
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="test@superuser.com",
                username="Uarname",
                password="",
                is_superuser=False,
            )

        # Here we test for email address validation when creating new user.
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="",
                username="Uarname",
                password="pass123",
            )

        # Here we test for is_staff validation when creating new user.
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="test@superuser.com",
                username="Uarname",
                password="pass123",
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="test@superuser.com",
                username="Uarname",
                password="pass123",
                is_active=False,
            )


    # Test new user.
    def test_new_user(self):
        db = get_user_model()           # Get Active User Model
        user = db.objects.create_user(
            'test@user.com',            # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        user.is_active = True
        user.is_verified = True

        user.save()
        
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.username, 'Username')
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_verified)

        # Testing our ValueError cases Custom AccountManager.
        # Testing whether a user can be created and have no username.
        with self.assertRaises(ValueError):
            db.objects.create_user(
                email="test@user.com",
                username="",
                password="pass123",
            )

        # Here we test for email address validation when creating new user.
        with self.assertRaises(ValueError):
            db.objects.create_user(
                email="",
                username="Uarname",
                password="pass123",
            )
