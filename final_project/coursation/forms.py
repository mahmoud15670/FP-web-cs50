from django.forms import ModelForm, forms
from .models import *

class Teacher_Form(ModelForm):
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        widgets = {
            'confirm':f
        }
        labels = {
            'username':'username',
            'password':'password',
            'email':'email address',
            'phone':'phone number'
        }

