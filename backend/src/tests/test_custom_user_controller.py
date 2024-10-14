from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from src.exceptions.response_exceptions import EntityNotFound


class TestCustomUserController(TestCase):
    api_client = APIClient()

    def setUp(self):
        user = User.objects.create_user("Authentication User")
        token = Token.objects.create(user=user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def tearDown(self):
        self.api_client.credentials()

    def test_success_custom_user_delete(self):
        with patch(
            "src.controllers.custom_user_controller.delete_custom_user", autospec=True
        ):
            response = self.api_client.delete("/user/1/")
            assert response.status_code == 204

    def test_failure_custom_user_delete_entity_not_found(self):
        response = self.api_client.delete("/user/0/")
        assert type(response) is EntityNotFound

    def test_failure_custom_user_delete_internal_server_error(self):
        with patch(
            "src.controllers.custom_user_controller.delete_custom_user",
            side_effect=Exception,
        ):
            response = self.api_client.delete("/user/1/")
            assert response.status_code == 500
