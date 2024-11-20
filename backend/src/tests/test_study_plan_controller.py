from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from src.exceptions.response_exceptions import (
    EntityNotFound,
    UnauthorizedAccess,
    UnprocessableEntity,
)
from src.models.study_plan_model import StudyPlan


class TestStudyPlanController(TestCase):
    api_client = APIClient()

    def setUp(self):
        # Criação do usuário para autenticação
        self.user = User.objects.create_user(
            "study_plan_user", "user@example.com", "password"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Criação do plano de estudo
        self.study_plan = StudyPlan.objects.create(
            title="Test Study Plan",
            visibility_id=1,  # Asegure-se de que o Domain com ID 1 exista
            author=self.user,
        )

    def tearDown(self):
        self.api_client.credentials()

    def test_success_create_study_plan(self):
        """Testa a criação de um plano de estudo com sucesso."""
        data = {
            "title": "New Study Plan",
            "visibility": 1,  # Asegure-se de que o Domain com ID 1 exista
        }
        response = self.api_client.post("/study_plan/", data)
        assert response.status_code == 200
        assert response.json()["title"] == "New Study Plan"

    def test_success_clone_study_plan(self):
        """Testa a clonagem de um plano de estudo com sucesso."""
        response = self.api_client.post(f"/study_plan/clone/{self.study_plan.id}/")
        assert response.status_code == 200
        assert response.json()["title"] == f"Cloned - {self.study_plan.title}"
        assert (
            response.json()["author"]["id"] == self.user.id
        )  # O autor da clonagem é o usuário logado

    def test_failure_clone_study_plan_permission_denied(self):
        """Testa a clonagem de um plano de estudo sem permissão (caso seja privado)."""
        # Crie outro usuário sem permissão
        other_user = User.objects.create_user(
            "other_user", "other@example.com", "password"
        )
        other_token = Token.objects.create(user=other_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.api_client.post(f"/study_plan/clone/{self.study_plan.id}/")
        assert response.status_code == 401  # UnauthorizedAccess

    def test_failure_clone_study_plan_not_found(self):
        """Testa a falha na clonagem de um plano de estudo que não existe."""
        response = self.api_client.post("/study_plan/clone/9999/")
        assert response.status_code == 404  # EntityNotFound

    def test_success_follow_study_plan(self):
        """Testa o seguimento de um plano de estudo com sucesso."""
        response = self.api_client.post(f"/study_plan/follow/{self.study_plan.id}/")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_failure_follow_study_plan_permission_denied(self):
        """Testa o seguimento de um plano de estudo sem permissão (caso seja privado)."""
        # Crie outro usuário sem permissão
        other_user = User.objects.create_user(
            "other_user", "other@example.com", "password"
        )
        other_token = Token.objects.create(user=other_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.api_client.post(f"/study_plan/follow/{self.study_plan.id}/")
        assert response.status_code == 401  # UnauthorizedAccess

    def test_failure_follow_study_plan_not_found(self):
        """Testa a falha ao seguir um plano de estudo inexistente."""
        response = self.api_client.post("/study_plan/follow/9999/")
        assert response.status_code == 404  # EntityNotFound

    def test_failure_create_study_plan_invalid_data(self):
        """Testa a criação de um plano de estudo com dados inválidos."""
        data = {
            "title": "",  # Título vazio
            "visibility": 1,  # Asegure-se de que o Domain com ID 1 exista
        }
        response = self.api_client.post("/study_plan/", data)
        assert response.status_code == 422  # UnprocessableEntity

    def test_failure_create_study_plan_internal_error(self):
        """Testa a falha interna ao criar um plano de estudo."""
        with patch(
            "src.services.study_plan_service.create_study_plan", side_effect=Exception
        ):
            data = {
                "title": "New Study Plan",
                "visibility": 1,
            }
            response = self.api_client.post("/study_plan/", data)
            assert response.status_code == 500  # InternalServerError
