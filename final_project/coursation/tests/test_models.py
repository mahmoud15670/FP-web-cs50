from django.test import TestCase
from coursation.models import *

class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(username='foo', password=123, email='mgh@mgh.com')
        return super().setUpTestData()

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        return super().setUp()

    def test_phone_max_length(self):
        phone_max_length =self.user._meta.get_field('phone').max_length
        self.assertEqual(phone_max_length, 11)

    def test_is_teacher(self):
        self.user.is_teacher = True
        self.assertTrue(self.user.is_teacher)


    def test_user_create_teacher(self):
        self.user.create_tracher()
        teacher = Techer.objects.get(pk=1)
        self.assertEqual(teacher.user.id, 1)
        self.assertTrue(teacher.user.is_teacher)
        self.assertFalse(teacher.user.is_student)

    def test_user_student_create(self):
        self.user.create_student()
        student = Student.objects.get(pk=1)
        self.assertEqual(student.user.id, 1)
        self.assertTrue(student.user.is_student)
        self.assertFalse(student.user.is_teacher)


    def test_stage(self):
        stage = Stage.objects.create(age_start=9, age_end=12, name='youth')
        self.assertIsNone(self.user.stage)
        self.user.stage = stage
        self.user.save()
        self.assertEqual(self.user.stage.name, 'youth')
        self.assertEqual(self.user.stage.age_start, 9)

    def test_section(self):
        section = Section.objects.create(name='programming')
        self.assertIsNone(self.user.section)
        self.user.section = section
        self.user.save()
        self.assertEqual(self.user.section.name, 'programming')


class StageTestCase():
    ...
