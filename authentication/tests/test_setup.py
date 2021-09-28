# APITestCase
from rest_framework.test import APITestCase

# Reverse Url - Route Generator.
from django.urls import reverse

# Faker
from faker import Faker

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register-user')
        self.login_url = reverse('login-user')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),                                     # Email
            'username': self.fake.email().split('@')[0],                  # Username
            'password': self.fake.email().split('@')[0]                   # Password
        }

        return super().setUp()

    def tearDown(self):

        return super().tearDown()