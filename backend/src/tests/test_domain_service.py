from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from src.models.domain_model import Domain
from src.services.domain_service import read_domain

MOCK_DOMAIN = {
    "id": 1,
    "name": "public",
    "type": "visibility",
    "relationship": "StudyPlan",
}


class ReadDomainTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_read_domain_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            read_domain(0)

    def test_read_domain_successfully(self):
        result = read_domain(1)
        self.assertDictEqual(result, MOCK_DOMAIN)
