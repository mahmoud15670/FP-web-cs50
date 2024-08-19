from django import forms
from .models import *

class User_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'phone', 'age', 'stage', 'section']
        widgets = {
            'password': forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
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
