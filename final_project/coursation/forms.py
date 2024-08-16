from django.forms import ModelForm
from .models import *

class Teacher_Form(ModelForm):
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        labels = {
            'username':'username',
            'password':'password',
            'email':'email address',
            'phone':'phone number'
        }

