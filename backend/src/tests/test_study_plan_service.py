from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from src.models.custom_user_model import CustomUser
from src.models.domain_model import Domain
from src.models.study_plan_model import StudyPlan
from src.services.study_plan_service import (
    create_study_plan,
    delete_study_plan,
    read_study_plan,
    update_study_plan,
)

VALID_STUDY_PLAN_DATA = [
    {"title": "Valid Plan 1", "visibility": "public"},
    {"title": "Valid Plan 2", "visibility": "private"},
    {"title": "Valid Plan 3"},
]

INVALID_STUDY_PLAN_DATA = [
    {"title": "Test Plan", "visibility": "invalid_visibility"},
    {"visibility": "public"},
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