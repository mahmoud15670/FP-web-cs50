from django.test import TestCase

from coursation.forms import *

class UserFormTestCase(TestCase):
    def confirm_password_field_label(self):
        form = User_Form()
        self.assertTrue(form.fields['confirm_password'].la)