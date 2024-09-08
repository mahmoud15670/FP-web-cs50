from django.test import TestCase

from coursation.views import *

class UserLoginViewTestCase(TestCase):
    def test_login_url(self):
        c = self.client()
        response = c.