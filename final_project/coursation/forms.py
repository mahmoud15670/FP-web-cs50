from django.forms import ModelForm, PasswordInput, CharField
from .models import *

class Teacher_Form(ModelForm):
    confirm_password = CharField(
        widget=PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        
        labels = {
            'username':'username',
            'password':'password',
            'email':'email address',
            'phone':'phone number'
        }

