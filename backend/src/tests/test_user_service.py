from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from src.models.custom_user import CustomUser
from src.services.custom_user_service import create_custom_user, delete_custom_user

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
