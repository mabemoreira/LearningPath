from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from src.exceptions.response_exceptions import EntityNotFound, InternalServerError


class TestLogoutController(TestCase):
    api_client = APIClient()

    def setUp(self):
        user = User.objects.create_user("Authentication User")
        token = Token.objects.create(user=user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def tearDown(self):
        self.api_client.credentials()

    def test_success_logout(self):
        with patch("src.controllers.logout_controller.logout", autospec=True):
            response = self.api_client.post("/auth/logout/")
            assert response.status_code == 204

    def test_failure_logout_entity_not_found(self):
        with patch(
            "src.controllers.logout_controller.logout",
            side_effect=ObjectDoesNotExist,
            autospec=True,
        ):
            response = self.api_client.post("/auth/logout/")
            assert type(response) is EntityNotFound

    def test_failure_logout_internal_server_error(self):
        with patch(
            "src.controllers.logout_controller.logout",
            side_effect=Exception,
        ):
            response = self.api_client.post("/auth/logout/")
            assert type(response) == InternalServerError
