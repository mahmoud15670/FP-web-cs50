from django.test import TestCase
from django.urls import reverse
from .models import *

# Create your tests here.
class LoginViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username='foo', password='123')
        return super().setUpTestData()
    
    def test_login_post(self):
        response = self.client.post(reverse('login'), data={
            "username":"foo",
            "password":"123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.json(), {'login':f'{response.wsgi_request.user.username} is logged in'})
    
    def test_faild_login(self):
        response = self.client.post(reverse('login'), data={
            "username":"bar",
            "password":"123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.json(), {'warrnin': 'username or password is incorect'})

class LogoutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username='foo', password='123')
        return super().setUpTestData()
    
    def test_logout(self):
        self.client.login(username="foo", password="123")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.json(), {'login':'foo is logged out'})

class RegisterViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user('bar', 'm@m.com', '123')
        return super().setUpTestData()
    def test_register(self):
        response = self.client.post(reverse('register'), data={
            "username":"foo",
            "password":"123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual('foo', User.objects.get(pk=2).username)
    
    def test_faild_register(self):
        response = self.client.post(reverse('register'), data={
            "username":"bar",
            "password":"123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'warrnin': 'username is already used'})
