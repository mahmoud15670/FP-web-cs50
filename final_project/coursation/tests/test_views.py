from django.test import TestCase

from coursation.views import *

class UserLoginViewTestCase(TestCase):
    def test_login_url(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('signin.html', [template.name for template in response.templates])
        self.assertEqual(response.resolver_match.func, login_view)
    
    def test_login_user(self):
        stage = Stage.objects.create(age_start=7, age_end=10, name="foo")
        section = Section.objects.create(name="foo")

        user = User.objects.create(username= "foo",
            phone= "1234567890",
            age= 7,
            stage= stage,
            exams= "dfdfd",
            section= section,
            rating= "2")
        user.set_password('123')
        user.save()
        response = self.client.post('/login', {'username':'foo', 'password':'123'})
        # self.assertEqual(response.status_code, 200)
        self.assertIn('index.html', [template.name for template in response.templates])
        