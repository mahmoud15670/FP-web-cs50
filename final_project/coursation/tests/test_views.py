from django.test import TestCase

from coursation.views import *

class UserLoginViewTestCase(TestCase):
    def test_login_url(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('signin.html', [template.name for template in response.templates])