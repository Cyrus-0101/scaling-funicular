from .test_setup import TestSetUp

# User Model
from ..models import User

class TestViews(TestSetUp):
    def test_register_new_user_with_no_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, 400)

    def test_register_new_user(self):
        res = self.client.post(self.register_url, self.user_data, format="json")

        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)


    def test_login_user_with_unverified_email(self):
        response = self.client.post(self.register_url, self.user_data, format="json")

        res = self.client.post(self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code, 401)

    def test_login_user_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")

        email = response.data['email']
        user = User.objects.get(email=email)

        user.is_active = True
        user.is_verified = True

        user.save()

        res = self.client.post(self.login_url, self.user_data, format="json")
        
        self.assertEqual(res.status_code, 200)
