from django.test import TestCase
from coursation.models import *

class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(username='foo', password=123, email='mgh@mgh.com')
        return super().setUpTestData()

    def test_first_name_label(self):
        user = User.objects.get(pk=1)
        first_name_label =user._meta.get_field('first_name').verbose_name
        self.assertEqual(first_name_label, 'first name')
