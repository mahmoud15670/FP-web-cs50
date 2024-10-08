import datetime

from django.test import TestCase

from coursation.models import *


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create(username="foo", password=123, email="mgh@mgh.com")
        return super().setUpTestData()

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        return super().setUp()

    def test_phone_max_length(self):
        phone_max_length = self.user._meta.get_field("phone").max_length
        self.assertEqual(phone_max_length, 11)

    def test_is_teacher(self):
        self.user.is_teacher = True
        self.assertTrue(self.user.is_teacher)

    def test_user_create_teacher(self):
        self.user.create_teacher()
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

    def test_user_set_stage1(self):
        test_stage1 = Stage.objects.create(age_start=7, age_end=10, name="foo")
        self.user.age = 9
        self.user.save()
        self.user.set_student_stage()
        self.assertEqual(self.user.stage, test_stage1)

    def test_user_set_stage2(self):
        Stage.objects.create(age_start=5, age_end=7, name="foo")
        self.user.age = 9
        self.user.save()
        self.user.set_student_stage()
        self.assertIsNone(self.user.stage)

    def test_user_set_stage3(self):
        Stage.objects.create(age_start=10, age_end=12, name="foo")
        self.user.age = 9
        self.user.save()
        self.user.set_student_stage()
        self.assertIsNone(self.user.stage)

    def test_stage(self):
        stage = Stage.objects.create(age_start=9, age_end=12, name="youth")
        self.assertIsNone(self.user.stage)
        self.user.stage = stage
        self.user.save()
        self.assertEqual(self.user.stage.name, "youth")
        self.assertEqual(self.user.stage.age_start, 9)

    def test_section(self):
        section = Section.objects.create(name="programming")
        self.assertIsNone(self.user.section)
        self.user.section = section
        self.user.save()
        self.assertEqual(self.user.section.name, "programming")


class StageTestCase(TestCase):
    def test_age_valid(self):
        stage = Stage.objects.create(age_start=7, age_end=10, name="foo")
        self.assertTrue(stage.age_isvalid()[0])
        self.assertEqual(
            stage.age_isvalid()[1], {"start": stage.age_start, "end": stage.age_end}
        )

    def test_age_invalid(self):
        stage1 = Stage.objects.create(age_start=2, age_end=5, name="foo")
        stage2 = Stage.objects.create(age_start=6, age_end=10, name="foo")
        stage3 = Stage.objects.create(age_start=82, age_end=87, name="foo")
        stage4 = Stage.objects.create(age_start=8, age_end=82, name="foo")
        stage5 = Stage.objects.create(age_start=18, age_end=8, name="foo")
        self.assertFalse(stage1.age_isvalid()[0])
        self.assertFalse(stage2.age_isvalid()[0])
        self.assertFalse(stage3.age_isvalid()[0])
        self.assertFalse(stage4.age_isvalid()[0])
        self.assertEqual(stage4.age_isvalid()[1], "age must in 7 to 80 years")
        self.assertFalse(stage5.age_isvalid()[0])
        self.assertEqual(
            stage5.age_isvalid()[1],
            f"age must in range of {stage5.age_start} and {stage5.age_end}",
        )


class CourseTestCase(TestCase):
    def setUp(self) -> None:
        Course.objects.create(
            name="foo",
            start_date=datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=2)
            ),
            stage=Stage.objects.create(age_start=7, age_end=10, name="foo"),
            duration="foo",
            about="fgsdfjgd",
        )
        return super().setUp()

    def test_course_is_started(self):
        course = Course.objects.get(pk=1)
        self.assertFalse(course.is_started())

    def test_course_is_not_started(self):
        course = Course.objects.get(pk=1)
        course.start_date = datetime.datetime.date(
            datetime.datetime.now() - datetime.timedelta(days=2)
        )
        course.save()
        self.assertTrue(course.is_started())

    def test_exam_count(self):
        course = Course.objects.get(pk=1)
        unit = Unit.objects.create(name="foo", course=course)
        exam1 = Exam.objects.create(
            date=datetime.datetime.date(datetime.datetime.now()),
            total=1,
            degree=100,
            duration=datetime.datetime.now(),
            question="jkh?",
            answer="sfsfs",
        )
        exam2 = Exam.objects.create(
            date=datetime.datetime.date(datetime.datetime.now()),
            total=1,
            degree=100,
            duration=datetime.datetime.now(),
            question="jkh?",
            answer="sfsfs",
        )
        lesson1 = Lesson.objects.create(unit=unit)
        lesson2 = Lesson.objects.create(unit=unit)
        lesson1.exam.add(exam1)
        lesson1.save()
        self.assertEqual(course.exam_count(), 1)
        lesson1.exam.add(exam2)
        lesson1.save()
        self.assertEqual(course.exam_count(), 2)
        lesson2.exam.add(exam1)
        lesson2.save()
        self.assertEqual(course.exam_count(), 3)


class UnitTestCase(TestCase):
    def setUp(self) -> None:
        Course.objects.create(
            name="foo",
            start_date=datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=2)
            ),
            stage=Stage.objects.create(age_start=7, age_end=10, name="foo"),
            duration="foo",
            about="fgsdfjgd",
        )
        Unit.objects.create(course=Course.objects.get(pk=1))
        Lesson.objects.create(unit=Unit.objects.get(pk=1))
        Lesson.objects.create(unit=Unit.objects.get(pk=1))
        return super().setUp()

    def test_get_video_count(self):
        lesson1 = Lesson.objects.get(pk=1)
        lesson2 = Lesson.objects.get(pk=2)
        unit = Unit.objects.get(pk=1)
        lesson1.video = "dfdfdf"
        lesson1.save()
        self.assertEqual(unit.get_video_count(), 1)
        lesson2.video = "dfdfdf"
        lesson2.save()
        self.assertEqual(unit.get_video_count(), 2)

    def test_get_read_count(self):
        lesson1 = Lesson.objects.get(pk=1)
        lesson2 = Lesson.objects.get(pk=2)
        unit = Unit.objects.get(pk=1)
        lesson1.read = "dfdfdf"
        lesson1.save()
        self.assertEqual(unit.get_read_count(), 1)
        lesson2.read = "dfdfdf"
        lesson2.save()
        self.assertEqual(unit.get_read_count(), 2)
