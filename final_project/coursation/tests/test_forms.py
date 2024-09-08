from django.test import TestCase

from coursation.forms import *

class UserFormTestCase(TestCase):
    def test_confirm_password_field_label(self):
        form = User_Form()
        self.assertTrue(form.fields['confirm_password'].label is None or form.fields['confirm_password'].label == 'confirm password')
        self.assertEqual(form.fields['confirm_password'])

    def test_clean_age(self):
        form = User_Form()