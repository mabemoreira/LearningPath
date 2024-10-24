from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from src.services.auth_service import login, logout

USER_MOCK = {
    "username": "Test User",
    "password": "1234",
    "email": "test.user@email.com",
}


class TestAuthService(TestCase):
    def setUp(self):
        self.user: User = User.objects.create_user(**USER_MOCK)

    def tearDown(self):
        self.user.delete()

    def test_login(self):
        result = login(USER_MOCK)
        self.assertEqual(result.get("token"), Token.objects.get(user=self.user).key)

        # Non existent user
        with self.assertRaises(ValidationError):
            result = login({})

    def test_logout(self):
        login(USER_MOCK)
        logout(self.user)
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)
