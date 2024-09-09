from contextlib import AbstractContextManager
from typing import Any
from django.test import TestCase

from coursation.views import *


class UserLoginViewTestCase(TestCase):

    def setUp(self) -> None:
        user = User.objects.create(username="foo")
        user.set_password("123")
        user.save()
        return super().setUp()

    def test_login_url(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("massage", response.context)
        self.assertEqual(response.resolver_match.func, login_view)
        self.assertTemplateUsed(response, "signin.html")

    def test_login_user(self):
        response = self.client.post(
            "/login", {"username": "foo", "password": "123"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "foo")
        self.assertRedirects(response, "/")
        self.assertTemplateUsed(response, "index.html")

    def test_invalid_login(self):
        response = self.client.post(
            "/login", {"username": "foo", "password": "1235"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("massage", response.context)
        self.assertEqual(
            response.context["massage"], "the user name or  password is incorrect"
        )
        self.assertTemplateUsed(response, "signin.html")


class LogoutViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='foo')
        user.set_password('123')
        user.save()
        self.client.login(username='foo', password='123')
        return super().setUp()

    def test_logout_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.get('/logout', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class IndexViewTestCase(TestCase):
    def setUp(self) -> None:
        teacher = User.objects.create(username='foo')
        teacher.set_password('123')
        teacher.create_teacher()
        teacher.save()
        student = User.objects.create(username='bar')
        student.set_password('123')
        student.create_student()
        student.save()
        admin = User.objects.create_superuser(username='baz', password='123')
        return super().setUp()

    def test_none_user_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('courses', response.context)
        self.assertIn('stage_list', response.context)
        self.assertIn('sections', response.context)
        self.assertIn('skills', response.context)
        self.assertTemplateUsed(response, 'index.html')

    def test_teacher_index(self):
        self.client.login(username='foo', password='123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_teacher)
        self.assertIn('teacher', response.context)
        self.assertNotIn('courses', response.context)
        self.assertTemplateUsed(response, 'teacher.html')

    def test_student_index(self):
        self.client.login(username='bar', password='123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_student)
        self.assertIn('student', response.context)
        self.assertIn('courses', response.context)
        self.assertTemplateUsed(response, 'student.html')

    def test_admin_index(self):
        self.client.login(username='baz', password='123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('courses', response.context)
        self.assertTemplateUsed(response, 'index.html')
class StageListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(5):
            Stage.objects.create(name=f'stage{i}')
        return super().setUpTestData()
    def test_get_list(self):
        response = self.client.get('/stage/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn('stage_list', response.context)
        self.assertEqual(response.context['stage_list'][0], Stage.objects.get(pk=1))
        self.assertTemplateUsed(response, 'index.html')
