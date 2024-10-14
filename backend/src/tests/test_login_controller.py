from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from src.exceptions.response_exceptions import (
    AuthenticationFailure,
    EntityNotFound,
    InternalServerError,
)


class TestLoginController(TestCase):
    api_client = APIClient()

    def test_success_login(self):
        with patch(
            "src.controllers.login_controller.login",
            autospec=True,
            return_value={},
        ):
            response = self.api_client.post("/auth/login/")
            assert response.status_code == 200

    def test_failure_login_authentication_failure(self):
        with patch(
            "src.controllers.login_controller.login",
            autospec=True,
            side_effect=ValidationError,
        ):
            response = self.api_client.post("/auth/login/")
            assert type(response) == AuthenticationFailure

    def test_failure_login_internal_server_error(self):
        with patch(
            "src.controllers.login_controller.login", autospec=True, side_effect=Exception
        ):
            response = self.api_client.post("/auth/login/")
            assert type(response) == InternalServerError
