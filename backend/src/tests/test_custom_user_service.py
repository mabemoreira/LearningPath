from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from src.models.custom_user_model import CustomUser
from src.services.custom_user_service import (
    create_custom_user,
    delete_custom_user,
    read_custom_user,
    update_custom_user,
)

VALID_USER_INPUT_MOCK = {
    "username": "testuser",
    "password": "TestPassword123",
    "email": "testuser@example.com",
}

INVALID_USER_INPUT_MOCKS = [
    # sem '.' no email
    {
        "username": "testuser",
        "password": "TestPassword123",
        "email": "testuser@example",
    },
    # sem '@' no email
    {
        "username": "testuser2",
        "password": "TestPassword123",
        "email": "testuserexample.com",
    },
    # username ja existente
    {
        "username": "testuser",
        "password": "TestPassword123",
        "email": "testuser@example.com",
    },
]

VALID_USER_UPDATE_MOCK = [
    # update email/username
    {
        "username": "testuser_updated",
        "email": "testuser@example.com",
    },
    # update username
    {
        "username": "testuser_updated2",
    },
    # update email
    {
        "email": "testuser@example.com",
    },
]

INVALID_USER_UPDATE_MOCKS = [
    # sem '.' no email
    {
        "username": "testuser_updated",
        "email": "testuser@example",
    },
    # sem '@' no email
    {
        "username": "testuser_updated2",
        "email": "testuserexample.com",
    },
    # username ja existente
    {
        "username": "testuser",
        "email": "testuser@example.com",
    },
]


class TestCreateCustomUserService(TestCase):
    def test_create_custom_user_valid_data(self):
        # Teste para usuario valido
        result = create_custom_user(VALID_USER_INPUT_MOCK)
        # Pega usuario no BD
        user = User.objects.get(username=VALID_USER_INPUT_MOCK["username"])
        custom_user = CustomUser.objects.get(user=user)
        # Valida retorno da funcao
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["user"]["email"], VALID_USER_INPUT_MOCK["email"])
        # Checa se usuario foi salvo corretamente
        self.assertEqual(user.email, VALID_USER_INPUT_MOCK["email"])
        self.assertTrue(user.check_password(VALID_USER_INPUT_MOCK["password"]))
        self.assertEqual(custom_user.user, user)

    def test_create_custom_user_invalid_data(self):
        # Teste para usuario invalido

        # cria usuario com username = 'testuser'
        create_custom_user(VALID_USER_INPUT_MOCK)
        for data in INVALID_USER_INPUT_MOCKS:
            with self.assertRaises(Exception):
                create_custom_user(data)


class ReadUserTestCase(TestCase):
    def setUp(self) -> None:
        create_custom_user(VALID_USER_INPUT_MOCK)

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_read_user_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            read_custom_user(0)
        with self.assertRaises(ObjectDoesNotExist):
            read_custom_user(2)

    def test_read_user_successfully(self):
        result = read_custom_user(1)
        assert result["id"] == 1
        assert result["user"]["email"] == VALID_USER_INPUT_MOCK["email"]


class TestDeleteCustomUserService(TestCase):
    def setUp(self) -> None:
        create_custom_user(VALID_USER_INPUT_MOCK)

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_custom_user_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            delete_custom_user(0)

    def test_custom_user_deleted_successfully(self):
        delete_custom_user(1)
        assert len(User.objects.filter(id=1)) == 0


class TestUpdateCustomUserService(TestCase):
    def setUp(self) -> None:
        create_custom_user(VALID_USER_INPUT_MOCK)

    def tearDown(self) -> None:
        if len(User.objects.filter(id=1)):
            User.objects.filter(id=1).delete()

    def test_update_custom_user_valid_data(self):
        user = User.objects.get(username=VALID_USER_INPUT_MOCK["username"])
        custom_user = CustomUser.objects.get(user=user)

        for data in VALID_USER_UPDATE_MOCK:
            result = update_custom_user(data, custom_user.id)
            user.refresh_from_db()
            custom_user.refresh_from_db()

            if "username" in data:
                self.assertEqual(user.username, data["username"])
            if "email" in data:
                self.assertEqual(user.email, data["email"])

    def test_update_custom_user_invalid_data(self):
        user = User.objects.get(username=VALID_USER_INPUT_MOCK["username"])
        custom_user = CustomUser.objects.get(user=user)

        for data in INVALID_USER_UPDATE_MOCKS:
            with self.assertRaises(Exception):
                update_custom_user(custom_user.id, data)
