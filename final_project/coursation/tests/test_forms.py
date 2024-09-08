from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from coursation.forms import *


class TeacherFormTestCase(TestCase):
    def test_fields(self):
        form = User_Form()
        self.assertTrue(
            form.fields["confirm_password"].label is None
            or form.fields["confirm_password"].label == "confirm password"
        )
        self.assertEqual(form.fields["age"].help_text, "")
        self.assertEqual(
            form.fields["stage"].help_text, "choose the stage you want to learn thim"
        )
        self.assertEqual(form.fields["section"].help_text, "choose your subject")


class StudentFormTestCase(TestCase):
    def test_fields(self):
        form = User_Student_Form()
        self.assertEqual(form.fields["age"].help_text, "age 7 to 80 years")

    def test_clean_age(self):
        stage = Stage.objects.create(age_start=7, age_end=10, name="foo")
        section = Section.objects.create(name="foo")

        data = {
            "username": "foo",
            "password": "12345678",
            "confirm_password": "12345678",
            "phone": "1234567890",
            "age": 7,
            "stage": stage.id,
            "exams": "dfdfd",
            "section": section.id,
            "rating": "2",
        }

        form1 = User_Student_Form(data=data)
        self.assertTrue(form1.is_valid())

        data["age"] = 80
        form2 = User_Student_Form(data=data)
        self.assertTrue(form2.is_valid())

        data["age"] = 5
        form3 = User_Student_Form(data=data)
        self.assertFalse(form3.is_valid())
        self.assertIn("age", form3.errors)
        self.assertEqual(form3.errors["age"][0], "Age must be between 7 and 80 years.")

        data["age"] = 81
        form4 = User_Student_Form(data=data)
        self.assertFalse(form4.is_valid())
        self.assertIn("age", form4.errors)
        self.assertEqual(form4.errors["age"][0], "Age must be between 7 and 80 years.")


class TeacherDeatilFormTestCase(TestCase):
    def test_fields(self):
        form = Teacher_form()
        self.assertTrue(
            form.fields["first_name"].label is None
            or form.fields["first_name"].label == "first name"
        )
        self.assertEqual(form.fields["cv"].help_text, "upload a cv in pdf format")
        self.assertEqual(
            form.fields["demo"].help_text,
            "upload a short video in mp4 format to intrduse your self and of your shar7",
        )

    def test_clean_cv(self):
        cv_file = SimpleUploadedFile("foo.pdf", b"df", "application/pdf")
        invalid_cv_file = SimpleUploadedFile("foo.txt", b"df", "text/plain")
        demo_file = SimpleUploadedFile("foo.mp4", b"gf", "video/mp4")
        data = {
            "first_name": "foo",
            "last_name": "bar",
        }
        form = Teacher_form(data=data, files={"cv": cv_file, "demo": demo_file})
        self.assertTrue(form.is_valid())
        form2 = Teacher_form(
            data=data, files={"cv": invalid_cv_file, "demo": demo_file}
        )
        self.assertFalse(form2.is_valid())
        self.assertIn("cv", form2.errors)
        self.assertNotIn("demo", form2.errors)
        self.assertEqual(form2.errors["cv"][0], "please upload a pdf file")

    def test_clean_demo(self):
        cv_file = SimpleUploadedFile("foo.pdf", b"df", "application/pdf")
        invalid_demo_file = SimpleUploadedFile("foo.txt", b"df", "text/plain")
        demo_file = SimpleUploadedFile("foo.mp4", b"gf", "video/mp4")
        data = {
            "first_name": "foo",
            "last_name": "bar",
        }
        form = Teacher_form(data=data, files={"cv": cv_file, "demo": demo_file})
        self.assertTrue(form.is_valid())
        form2 = Teacher_form(
            data=data, files={"cv": cv_file, "demo": invalid_demo_file}
        )
        self.assertFalse(form2.is_valid())
        self.assertIn("demo", form2.errors)
        self.assertNotIn("cv", form2.errors)
        self.assertEqual(form2.errors["demo"][0], "please upload a mp4 video")
        form3 = Teacher_form(
            data=data, files={"cv": invalid_demo_file, "demo": invalid_demo_file}
        )
        self.assertFalse(form3.is_valid())
        self.assertIn("demo", form3.errors)
        self.assertIn("cv", form3.errors)
        self.assertEqual(form3.errors["demo"][0], "please upload a mp4 video")
        self.assertEqual(form3.errors["cv"][0], "please upload a pdf file")
