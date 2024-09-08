from django.test import TestCase

from coursation.views import *

class UserLoginViewTestCase(TestCase):
    def test_login_url(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('signin.html', [template.name for template in response.templates])
        self.assertEqual(response.resolver_match.func, login_view)
    
    def test_login_user(self):
        user = User.objects.create(username= "foo")
        user.set_password('123')
        user.save()
        response = self.client.post('/login', {'username':'foo', 'password':'123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'foo')
        self.assertRedirects(response, '/')
        self.assertIn('index.html', [template.name for template in response.templates])
    
    def test_invalid_login(self):
        user = User.objects.create(username= "foo")
        user.set_password('123')
        user.save()
        response = self.client.post('/login', {'username':'foo', 'password':'1235'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('')
        