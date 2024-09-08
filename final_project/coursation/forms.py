from django import forms
from django.core.exceptions import ValidationError

from .models import *


class User_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "email",
            "phone",
            "age",
            "stage",
            "section",
        ]
        widgets = {
            "password": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            "age": forms.NumberInput(attrs={"max": 80, "min": 7}),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age not in range(7, 81):
            raise ValidationError("age must in 7 to 80 years")
        return age
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class User_Student_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "email", "phone", "age"]
        widgets = {
            "password": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            "age": forms.NumberInput(attrs={"max": 80, "min": 7}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class Teacher_form(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Techer
        fields = ["first_name", "last_name", "cv", "demo"]

    def clean_cv(self):
        cv = self.cleaned_data["cv"]
        if cv.content_type != "application/pdf":
            raise ValidationError("please upload a pdf file")
        return cv

    def clean_demo(self):
        demo = self.cleaned_data["demo"]
        if demo.content_type != "video/mp4":
            raise ValidationError("please upload a mp4 video")
        return demo


class Group_Form(forms.ModelForm):
    class Meta:
        model = Groub
        fields = ["name", "count"]


class Course_Form(forms.ModelForm):

    start_date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Course
        fields = "__all__"
        exclude = ["teacher", "student", "cirtification", "review"]
        widgets = {"skill": forms.CheckboxSelectMultiple()}


class Unit_Form(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "goal"]


class Lesson_Form(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        exclude = ["unit", "exam"]
