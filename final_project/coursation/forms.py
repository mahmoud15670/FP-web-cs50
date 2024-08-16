from django.forms import ModelForm, PasswordInput, CharField, TextInput
from .models import *

class Teacher_Form(ModelForm):
    confirm_password = CharField(
        widget=PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = Techer
        fields  = ['username', 'password', 'email','phone']
        widget = {
            'username':TextInput(attrs={'autocomplete': 'off','placeholder': 'Enter your username'})
        }

