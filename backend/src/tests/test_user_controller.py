from unittest.mock import patch

from django.test import TestCase
from django.test.client import Client
from src.exceptions.response_exceptions import EntityNotFound


class TestDeleteCustomUserController(TestCase):
    client = Client()

    def test_custom_user_not_found(self):
        response = self.client.delete("/user/1/")
        assert type(response) is EntityNotFound

    def test_custom_user_deleted_successfully(self):
        with patch(
            "src.controllers.custom_user_controller.delete_custom_user", autospec=True
        ):
            response = self.client.delete("/user/1/")
            assert response.status_code == 204

    def test_internal_server_error(self):
        with patch(
            "src.controllers.custom_user_controller.delete_custom_user",
            side_effect=Exception,
        ):
            response = self.client.delete("/user/1/")
            assert response.status_code == 500
