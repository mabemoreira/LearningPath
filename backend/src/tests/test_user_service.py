import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from src.models.custom_user import (
    CustomUser,
    CustomUserSerializer,
    UserSerializer,
)
from src.services.custom_user_service import create_custom_user


class TestCreateCustomUser(TestCase):

    @patch("src.models.custom_user.UserSerializer")
    @patch("src.models.custom_user.CustomUserSerializer")
    @patch("django.contrib.auth.models.User.objects.create_user")
    @patch("src.models.custom_user.CustomUser.objects.create")
    def test_create_custom_user(
        self,
        mock_create_custom_user,
        mock_create_user,
        mock_custom_user_serializer,
        mock_user_serializer,
    ):
        # Mock the data
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
        }

        # Mock the UserSerializer to always return valid
        mock_user_serializer.return_value.is_valid.return_value = True

        # Mock the User creation
        mock_user = User(username=data["username"], email=data["email"])
        mock_create_user.return_value = mock_user

        # Mock the CustomUser creation
        mock_custom_user = CustomUser(user=mock_user)
        mock_create_custom_user.return_value = mock_custom_user

        # Mock the CustomUserSerializer to return the expected data
        expected_serialized_data = {"id": 1, "username": "testuser"}
        mock_custom_user_serializer.return_value.data = expected_serialized_data

        # Call the function
        result = create_custom_user(data)

        # Assertions
        mock_user_serializer.assert_called_once_with(data=data)
        mock_user_serializer.return_value.is_valid.assert_called_once_with(
            raise_exception=True
        )
        mock_create_user.assert_called_once_with(**data)
        mock_create_custom_user.assert_called_once_with(user=mock_user)
        mock_custom_user_serializer.assert_called_once_with(mock_custom_user)
        self.assertEqual(result, expected_serialized_data)


if __name__ == "__main__":
    unittest.main()
