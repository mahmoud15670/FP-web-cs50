from django.test import TestCase, Client
from .models import *

class UserTestCase(TestCase):
    def setUp(self) -> None:
        mgh = User.objects.create(username='mgh', password=123, email='mgh@mgh.com', is_teacher=True)
        Techer.objects.create(user=mgh)

        return super().setUp()
    def test_user_name(self):
        mgh = User.objects.get(username='mgh')
        teacher_mgh = Techer.objects.get(user=mgh)
        self.assertEqual(mgh.email, 'mgh@mgh.com')
        self.assertEqual(teacher_mgh.user.is_teacher, True)

class LoginTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='foo', password=123, email='mgh@mgh.com')
        return super().setUp()

    def test_login(self):
        responce = self.client.get('')
        self.assertEqual(responce.status_code, 200)
        self.assertEqual()
        user = self.client.login(username='foo', password=123)
        self.assertTrue(user)



