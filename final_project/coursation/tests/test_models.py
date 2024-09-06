from django.test import TestCase
from coursation.models import *

class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(username='foo', password=123, email='mgh@mgh.com')
        return super().setUpTestData()


    def test_phone_max_length(self):
        user = User.objects.get(pk=1)
        phone_max_length =user._meta.get_field('phone').max_length
        self.assertEqual(phone_max_length, 11)

    def test_is_teacher(self):
        user = User.objects.get(pk=1)
        user.is_teacher = True
        self.assertTrue(user.is_teacher)
