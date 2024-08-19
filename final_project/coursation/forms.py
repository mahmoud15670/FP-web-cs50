from django import forms
from .models import *

class User_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'new-password', 'placeholder':'your user name'}),
            'password': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'your password'}),
            'email': forms.EmailInput(attrs={'placeholder':'your email'}),
            'phone': forms.TextInput(attrs={'placeholder':'your phone'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class Teacher_form(forms.ModelForm):
    class Meta:
        model = Techer
        fields = [ 'cv', 'demo']

class User_detail_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['age', 'stage', 'section']


class Student_form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm your password'})
    )
    class Meta:
        model = Student
        fields = ['progress']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
