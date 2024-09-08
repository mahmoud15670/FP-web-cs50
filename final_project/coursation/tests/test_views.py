from django.test import TestCase

from coursation.views import *

class UserLoginViewTestCase(TestCase):
    def test_login_url(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('signin.html', [template.name for template in response.templates])
    def test_login_user(self):
        User.objects.create(username='foo', password='123')
        response = self.client.login(username='foo', password='123')
        self.assertEqual(response.s)