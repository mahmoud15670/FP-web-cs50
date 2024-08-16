from django.forms import ModelForm, PasswordInput, CharField
from .models import *

class Teacher_Form(ModelForm):
    confirm_password = CharField(widget=PasswordInput())
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        
        labels = {
            'username':'username',
            'password':'password',
            'email':'email address',
            'phone':'phone number'
        }

