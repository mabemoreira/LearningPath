from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan
from src.services.study_plan_service import (
    clone_study_plan,
    create_study_plan,
    delete_study_plan,
    follow_study_plan,
    read_study_plan,
    unfollow_study_plan,
    update_study_plan,
)

from ..models.user_follows_study_plan_model import UserFollowsStudyPlan

VALID_STUDY_PLAN_DATA = [
    {"title": "1", "visibility": "public"},
    {"title": "Valid Plan 2", "visibility": "private"},
    {
        "title": "áBCDEFGHIJKLMNôPQRSTUVWXçZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFG",
        "visibility": "private",
    },
]
# vamos de classe de equivalencia, o título tem que existir e ele deve ser composto apenas por letras (acentuadas ou não), números ou " ", além de ter no máximo 255 caracteres
INVALID_STUDY_PLAN_DATA = [
    {"title": "Test Plan", "visibility": "invalid_visibility"},
    {"title": "", "visibility": "public"},
    {
        "title": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLL0ASLEIKKJW",
        "visibility": "public",
    },
    {"title": "ol@", "visibility": "public"},
    {
        "title": "$BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEF",
        "visibility": "private",
    },
]


UPDATED_STUDY_PLAN_DATA = {
    "title": "Updated Study Plan Title",
    "visibility": "private",
}


class TestCreateStudyPlanService(TestCase):
    def setUp(self) -> None:
        # Setting up the necessary user for the test
        self.user = User.objects.create_user(
            username="testuser", password="TestPassword123"
        )
        self.custom_user = CustomUser.objects.create(user=self.user)

    def tearDown(self) -> None:
        if len(User.objects.filter(id=self.user.id)):
            User.objects.filter(id=self.user.id).delete()
        if len(CustomUser.objects.filter(id=self.custom_user.id)):
            CustomUser.objects.filter(id=self.custom_user.id).delete()

    def test_create_study_plan_valid_data(self):
        for data in VALID_STUDY_PLAN_DATA:
            # Calling the service to create the study plan
            result = create_study_plan(data, self.user)

            # Ensure the StudyPlan was created
            study_plan = StudyPlan.objects.get(id=result["id"])

            # Validate the response
            self.assertEqual(result["id"], study_plan.id)
            self.assertEqual(result["title"], study_plan.title)
            self.assertEqual(
                result["visibility"]["id"], study_plan.visibility.id
            )  # Ensure visibility is correct
            self.assertEqual(
                study_plan.author.user.username, "testuser"
            )  # Validate that the correct user is set

    def test_create_study_plan_invalid_data(self):
        # Invalid data test cases
        for data in INVALID_STUDY_PLAN_DATA:
            with self.assertRaises(Exception):
                create_study_plan(data, self.user)


class TestReadStudyPlanService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="private"),
            author=self.user,
        )

    def test_read_study_plan_successfully(self):
        result = read_study_plan(self.study_plan.id, self.user.user)
        self.assertEqual(result["id"], self.study_plan.id)
        self.assertEqual(result["title"], self.study_plan.title)

    def test_read_study_plan_no_access_permission(self):
        another_user = User.objects.create(username="otheruser")
        with self.assertRaises(PermissionDenied):
            read_study_plan(self.study_plan.id, another_user)


class TestDeleteStudyPlanService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="public"),
            author=self.user,
        )

    def test_delete_study_plan_successfully(self):
        delete_study_plan(self.study_plan.id, self.user.user)
        self.study_plan.refresh_from_db()
        self.assertTrue(self.study_plan.deleted)

    def test_delete_study_plan_no_permission(self):
        another_user = User.objects.create(username="otheruser")
        with self.assertRaises(PermissionDenied):
            delete_study_plan(self.study_plan.id, another_user)


class TestUpdateStudyPlanService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="private"),
            author=self.user,
        )

    def test_update_study_plan_valid_data(self):
        result = update_study_plan(
            UPDATED_STUDY_PLAN_DATA, self.study_plan.id, self.user.user
        )
        self.study_plan.refresh_from_db()
        self.assertEqual(result["title"], UPDATED_STUDY_PLAN_DATA["title"])
        self.assertEqual(
            self.study_plan.visibility.name, UPDATED_STUDY_PLAN_DATA["visibility"]
        )

    def test_update_study_plan_no_permission(self):
        another_user = User.objects.create(username="otheruser")
        with self.assertRaises(PermissionDenied):
            update_study_plan(UPDATED_STUDY_PLAN_DATA, self.study_plan.id, another_user)


class TestFollowStudyPlanService(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            user=User.objects.create(username="testuser1")
        )
        self.user2 = CustomUser.objects.create(
            user=User.objects.create(username="testuser2")
        )
        self.private_study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="private"),
            author=self.user1,
        )
        self.public_study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="public"),
            author=self.user1,
        )

    def test_follow_study_plan_successfully(self):
        study_plan_id = self.public_study_plan.id
        result = follow_study_plan(dict(), study_plan_id, self.user2.user)
        follow = UserFollowsStudyPlan.objects.get(
            user=self.user2, study_plan=self.public_study_plan
        )
        self.assertEqual(result["study_plan"]["id"], study_plan_id)
        self.assertEqual(follow.id, result["id"])
        self.assertEqual(follow.user.id, self.user2.id)

    def test_follow_study_plan_no_permission(self):
        with self.assertRaises(PermissionDenied):
            follow_study_plan(dict(), self.private_study_plan.id, self.user2.user)


class TestCloneStudyPlanService(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            user=User.objects.create(username="testuser")
        )
        self.study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="private"),
            author=self.user,
        )

    def test_clone_study_plan_successfully(self):
        result = clone_study_plan(
            {"visibility": "public"}, self.user.user, self.study_plan.id
        )
        self.assertNotEqual(result["id"], self.study_plan.id)
        self.assertEqual(result["title"], f"Cópia de {self.study_plan.title}")

    def test_clone_study_plan_no_permission(self):
        another_user = User.objects.create(username="otheruser")
        with self.assertRaises(PermissionDenied):
            clone_study_plan(dict(), another_user, self.study_plan.id)


class TestFollowStudyPlanService(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            user=User.objects.create(username="testuser1")
        )
        self.user2 = CustomUser.objects.create(
            user=User.objects.create(username="testuser2")
        )
        self.study_plan = StudyPlan.objects.create(
            title=VALID_STUDY_PLAN_DATA[0]["title"],
            visibility=Domain.objects.get(name="public"),
            author=self.user1,
        )

    def test_follow_study_plan(self):
        # Executa a função follow
        response = follow_study_plan({}, self.study_plan.id, self.user2.user)

        # Verifica se o usuário está seguindo o plano
        self.assertTrue(
            UserFollowsStudyPlan.objects.filter(
                user=self.user2, study_plan=self.study_plan
            ).exists()
        )
        self.assertEqual(response["study_plan"], self.study_plan.id)

    def test_unfollow_study_plan(self):
        # Primeiro, seguir o plano
        follow_study_plan({}, self.study_plan.id, self.user2.user)

        # Depois, remover o follow
        unfollow_study_plan({}, self.study_plan.id, self.user2.user)

        # Verificar se o follow foi removido
        self.assertFalse(
            UserFollowsStudyPlan.objects.filter(
                user=self.user2, study_plan=self.study_plan
            ).exists()
        )
