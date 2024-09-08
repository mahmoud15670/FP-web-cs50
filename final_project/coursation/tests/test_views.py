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


