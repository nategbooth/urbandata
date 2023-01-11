from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        print("User:", User)
        user = User.objects.create_user(email='hello@fakeurl.com', password='fakepassword')
        print("user:", user)
        self.assertEqual(user.email, 'hello@fakeurl.com')
