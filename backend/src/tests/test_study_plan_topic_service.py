from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.test import TestCase
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan
from src.models.study_plan_topic_model import StudyPlanTopic
from src.services.study_plan_topic_service import (
    create_study_plan_topic,
    delete_study_plan_topic,
    read_study_plan_topic,
    update_study_plan_topic,
)

VALID_STUDY_PLAN_TOPIC_DATA = [
    {"title": "Valid Topic 1", "description": "Description 1"},
    {"title": "Valid Topic 2", "description": "Description 2"},
    {"title": "Valid Topic 3", "description": "Description 3"},
]

INVALID_STUDY_PLAN_TOPIC_DATA = [
    {"title": "", "description": "Description without title"},
    {"description": "Description without title"},
]

UPDATED_STUDY_PLAN_TOPIC_DATA = {
    "title": "Updated Topic Title",
    "description": "Updated Description",
}


class TestCreateStudyPlanTopicService(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="TestPassword123"
        )
        self.custom_user = CustomUser.objects.create(user=self.user)
        self.study_plan = StudyPlan.objects.create(
            title="Test Plan",
            visibility=Domain.objects.get(name="public"),
            author=self.custom_user,
        )

    def tearDown(self) -> None:
        User.objects.filter(id=self.user.id).delete()
        CustomUser.objects.filter(id=self.custom_user.id).delete()
        StudyPlan.objects.filter(id=self.study_plan.id).delete()

    @patch("src.services.study_plan_topic_service.StudyPlanTopic.objects.create")
    @patch("src.services.study_plan_topic_service.StudyPlanTopicSerializer")
    def test_create_study_plan_topic_valid_data(self, mock_serializer, mock_create):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            "id": 1,
            "title": "Valid Topic 1",
            "description": "Description 1",
        }
        mock_create.return_value = StudyPlanTopic(
            id=1,
            title="Valid Topic 1",
            description="Description 1",
            study_plan=self.study_plan,
        )

        for data in VALID_STUDY_PLAN_TOPIC_DATA:
            result = create_study_plan_topic(data, self.study_plan.id)
            self.assertEqual(result["id"], 1)
            self.assertEqual(result["title"], "Valid Topic 1")
            self.assertEqual(result["description"], "Description 1")

    @patch("src.services.study_plan_topic_service.StudyPlanTopicSerializer")
    def test_create_study_plan_topic_invalid_data(self, mock_serializer):
        mock_serializer.return_value.is_valid.side_effect = Exception("Invalid data")

        for data in INVALID_STUDY_PLAN_TOPIC_DATA:
            with self.assertRaises(Exception):
                create_study_plan_topic(data, self.study_plan.id)


class TestReadStudyPlanTopicService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title="Test Plan",
            visibility=Domain.objects.get(name="private"),
            author=self.user,
        )
        self.study_plan_topic = StudyPlanTopic.objects.create(
            title="Test Topic",
            description="Test Description",
            study_plan=self.study_plan,
        )

    @patch("src.services.study_plan_topic_service.StudyPlanTopic.objects.get")
    @patch("src.services.study_plan_topic_service.StudyPlanTopicSerializer")
    def test_read_study_plan_topic_successfully(self, mock_serializer, mock_get):
        mock_get.return_value = self.study_plan_topic
        mock_serializer.return_value.data = {
            "id": self.study_plan_topic.id,
            "title": self.study_plan_topic.title,
            "description": self.study_plan_topic.description,
        }

        result = read_study_plan_topic(self.study_plan_topic.id, self.user.user)
        self.assertEqual(result["id"], self.study_plan_topic.id)
        self.assertEqual(result["title"], self.study_plan_topic.title)
        self.assertEqual(result["description"], self.study_plan_topic.description)

    @patch("src.services.study_plan_topic_service.StudyPlanTopic.objects.get")
    def test_read_study_plan_topic_no_access_permission(self, mock_get):
        mock_get.return_value = self.study_plan_topic
        another_user = User.objects.create(username="otheruser")

        with self.assertRaises(PermissionDenied):
            read_study_plan_topic(self.study_plan_topic.id, another_user)


class TestDeleteStudyPlanTopicService(TestCase):
    def setUp(self):
        # Configuração do ambiente
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.domain = Domain.objects.create(name="public")
        self.study_plan = StudyPlan.objects.create(
            title="Test Plan",
            visibility=self.domain,
            author=self.user,
        )
        self.study_plan_topic = StudyPlanTopic.objects.create(
            title="Test Topic",
            description="Test Description",
            study_plan=self.study_plan,
        )

    def test_delete_study_plan_topic_successfully(self):
        # Certifica-se de que o objeto existe
        self.assertTrue(
            StudyPlanTopic.objects.filter(id=self.study_plan_topic.id).exists()
        )

        # Chama a função para deletar o tópico
        delete_study_plan_topic(self.study_plan_topic.id, self.user.user)

        # Verifica se o objeto foi deletado
        with self.assertRaises(ObjectDoesNotExist):
            StudyPlanTopic.objects.get(id=self.study_plan_topic.id)

    @patch("src.models.StudyPlan.access_allowed")
    def test_delete_study_plan_topic_no_permission(self, mock_access_allowed):
        # Configura o mock para retornar False
        mock_access_allowed.return_value = False

        # Cria um outro usuário sem permissão
        another_user = User.objects.create(username="otheruser")

        # Verifica se a exceção PermissionDenied é levantada
        with self.assertRaises(PermissionDenied):
            delete_study_plan_topic(self.study_plan_topic.id, another_user)

        # Verifica que o mock foi chamado corretamente
        mock_access_allowed.assert_called_once_with(another_user)


class TestUpdateStudyPlanTopicService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title="Test Plan",
            visibility=Domain.objects.get(name="private"),
            author=self.user,
        )
        self.study_plan_topic = StudyPlanTopic.objects.create(
            title="Test Topic",
            description="Test Description",
            study_plan=self.study_plan,
        )

    @patch("src.services.study_plan_topic_service.StudyPlanTopic.objects.get")
    @patch("src.services.study_plan_topic_service.StudyPlanTopicSerializer")
    def test_update_study_plan_topic_valid_data(self, mock_serializer, mock_get):
        mock_get.return_value = self.study_plan_topic
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            "id": self.study_plan_topic.id,
            "title": UPDATED_STUDY_PLAN_TOPIC_DATA["title"],
            "description": UPDATED_STUDY_PLAN_TOPIC_DATA["description"],
        }

        result = update_study_plan_topic(
            self.study_plan_topic.id, UPDATED_STUDY_PLAN_TOPIC_DATA, self.user.user
        )
        self.assertEqual(result["title"], UPDATED_STUDY_PLAN_TOPIC_DATA["title"])
        self.assertEqual(
            result["description"], UPDATED_STUDY_PLAN_TOPIC_DATA["description"]
        )

    @patch("src.services.study_plan_topic_service.StudyPlanTopic.objects.get")
    def test_update_study_plan_topic_no_permission(self, mock_get):
        mock_get.return_value = self.study_plan_topic
        another_user = User.objects.create(username="otheruser")

        with self.assertRaises(PermissionDenied):
            update_study_plan_topic(
                self.study_plan_topic.id, UPDATED_STUDY_PLAN_TOPIC_DATA, another_user
            )
