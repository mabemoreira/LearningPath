from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class TestEndpointsAuthentication(TestCase):
    api_client = APIClient()

    def test_endpoints_authentication_user(self):
        with (
            patch(
                "src.controllers.custom_user_controller.create_custom_user",
                autospec=True,
                return_value={},
            ),
            patch(
                "src.controllers.custom_user_controller.read_custom_user",
                autospec=True,
                return_value={},
            ),
            patch(
                "src.controllers.custom_user_controller.delete_custom_user", autospec=True
            ),
            patch(
                "src.controllers.custom_user_controller.update_custom_user",
                autospec=True,
                return_value={},
            ),
        ):
            # asserts all endpoints, except POST, require authentication
            assert self.api_client.post("/user/").status_code == 200
            assert self.api_client.put("/user/1/").status_code == 401
            assert self.api_client.get("/user/1/").status_code == 401
            assert self.api_client.delete("/user/1/").status_code == 401

    def test_endpoints_authentication_login(self):
        with patch(
            "src.controllers.login_controller.login", autospec=True, return_value={}
        ):
            # asserts all endpoints, except POST, require authentication
            assert self.api_client.post("/auth/login/").status_code == 200

    def test_endpoints_authentication_logout(self):
        self.api_client.credentials()  # logout after setup
        with patch(
            "src.controllers.logout_controller.logout", autospec=True, return_value={}
        ):
            # asserts all endpoints, except POST, require authentication
            assert self.api_client.post("/auth/logout/").status_code == 401
