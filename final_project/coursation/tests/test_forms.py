from django.test import TestCase

from coursation.forms import *

class UserFormTestCase(TestCase):
    def test_confirm_password_field_label(self):
        form = User_Form()
        self.assertTrue(form.fields['confirm_password'].label is None or form.fields['confirm_password'].label == 'confirm password')
        self.assertEqual(form.fields['age'].help_text, 'age 7 to 80 years')
        self.assertEqual(form.fields['stage'].help_text, "choose the stage you want to learn thim")
        self.assertEqual(form.fields['section'].help_text, "choose your subject")

    def test_clean_age(self):
        form1 = User_Form(data={'uaername':'foo', 'password':123, 'eamil':'foo@gamil.com', 'phone':'123', 'age': 7})
        self.assertTrue(form1.is_valid())
        # form2 = User_Form({'age':80})
        # self.assertTrue(form2.is_valid())
        # form3 = User_Form({'age':5})
        # self.assertRaisesMessage(form3.is_valid(),"age must in 7 to 80 years")
        # form4 = User_Form({'age':81})
        # self.assertRaisesMessage(form4.is_valid(),"age must in 7 to 80 years")