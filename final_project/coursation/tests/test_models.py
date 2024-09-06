from django.test import TestCase
from coursation.models import *

class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(username='foo', password=123, email='mgh@mgh.com')
        return super().setUpTestData()

    
