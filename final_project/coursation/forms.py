from django.forms import ModelForm, PasswordInput
from .models import *

class Teacher_Form(ModelForm):
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        widgets = {
            'confirm':PasswordInput()
        }
        labels = {
            'username':'username',
            'password':'password',
            'email':'email address',
            'phone':'phone number'
        }

