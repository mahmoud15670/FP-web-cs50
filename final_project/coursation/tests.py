from django.test import TestCase
from .models import *

class UserTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='mgh', password=123, email='mgh@mgh.com')

        return super().setUp()
    def test_user_name(self):
        mgh = User.objects.get(username='mgh')
        self.assertEqual(mgh.email, 'mgh@mgh.com')
