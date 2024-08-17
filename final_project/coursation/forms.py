from django import forms
from .models import *

class Teacher_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = Techer
        fields = ['username', 'password', 'email', 'phone']
        exclude = ['activation']

        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off','placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Enter your password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),

        }


class Teacher_detail_form(forms.ModelForm):
    class Meta:
        model = Techer
        fields = ['first_name', 'last_name', 'age', 'stage', 'section', 'cv', 'demo']
        widgets = {
            'first_name': forms.TextInput(required=True),
            'last_name': forms.TextInput(required=True)
        }
