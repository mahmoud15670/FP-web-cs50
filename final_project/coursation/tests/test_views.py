from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from coursation.views import *


class UserLoginViewTestCase(TestCase):

    def setUp(self) -> None:
        user = User.objects.create(username="foo")
        user.set_password("123")
        user.save()
        return super().setUp()

    def test_login_url(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("massage", response.context)
        self.assertEqual(response.resolver_match.func, login_view)
        self.assertTemplateUsed(response, "signin.html")

    def test_login_user(self):
        response = self.client.post(
            "/login", {"username": "foo", "password": "123"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "foo")
        self.assertRedirects(response, "/")
        self.assertTemplateUsed(response, "index.html")

    def test_invalid_login(self):
        response = self.client.post(
            "/login", {"username": "foo", "password": "1235"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("massage", response.context)
        self.assertEqual(
            response.context["massage"], "the user name or  password is incorrect"
        )
        self.assertTemplateUsed(response, "signin.html")


class LogoutViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username="foo")
        user.set_password("123")
        user.save()
        self.client.login(username="foo", password="123")
        return super().setUp()

    def test_logout_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.get("/logout", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "index.html")


class IndexViewTestCase(TestCase):
    def setUp(self) -> None:
        teacher = User.objects.create(username="foo")
        teacher.set_password("123")
        teacher.create_teacher()
        student = User.objects.create(username="bar")
        student.set_password("123")
        student.create_student()
        User.objects.create_superuser(username="baz", password="123")
        return super().setUp()

    def test_none_user_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("courses", response.context)
        self.assertIn("stage_list", response.context)
        self.assertIn("sections", response.context)
        self.assertIn("skills", response.context)
        self.assertTemplateUsed(response, "index.html")

    def test_teacher_index(self):
        self.client.login(username="foo", password="123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_teacher)
        self.assertIn("teacher", response.context)
        self.assertNotIn("courses", response.context)
        self.assertTemplateUsed(response, "teacher.html")

    def test_student_index(self):
        self.client.login(username="bar", password="123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_student)
        self.assertIn("student", response.context)
        self.assertIn("courses", response.context)
        self.assertTemplateUsed(response, "student.html")

    def test_admin_index(self):
        self.client.login(username="baz", password="123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("courses", response.context)
        self.assertTemplateUsed(response, "index.html")


class StageListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(5):
            Stage.objects.create(name=f"stage{i}", age_start=8, age_end=18)
        return super().setUpTestData()

    def test_get_list(self):
        response = self.client.get("/stage/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("stage_list", response.context)
        self.assertEqual(response.context["stage_list"].count(), 5)
        self.assertEqual(
            response.context["stage_list"][0], Stage.objects.get(pk=1))
        self.assertTemplateUsed(response, "index.html")


class TeacherRegisterViewTestCase(TestCase):
    def setUp(self) -> None:
        stage = Stage.objects.create(age_start=7, age_end=12, name="foo")
        section = Section.objects.create(name="foo")
        self.data = {
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

        return super().setUp()

    def test_teacher_register_get(self):
        response = self.client.get("/teacher/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["form"], User_Form)
        self.assertTemplateUsed(response, "teacher_register.html")

    def test_teacher_register_post(self):
        response = self.client.post(
            "/teacher/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_teacher)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "index.html")

    def test_teacher_register_invslid_username(self):
        self.data["username"] = "****"
        response = self.client.post(
            "/teacher/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["username"][0],
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
        )
        self.assertTemplateUsed(response, "teacher_register.html")

    def test_teacher_register_invslid_paswords(self):
        self.data["password"] = "123"
        self.data["confirm_password"] = "1235"
        response = self.client.post(
            "/teacher/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["confirm_password"][0],
            "Passwords do not match.",
        )
        self.assertTemplateUsed(response, "teacher_register.html")


class StudentRegisterViewTestCase(TestCase):
    def setUp(self) -> None:
        stage = Stage.objects.create(age_start=7, age_end=12, name="foo")
        section = Section.objects.create(name="foo")
        self.data = {
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

        return super().setUp()

    def test_student_register_get(self):
        response = self.client.get("/student/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["form"], User_Student_Form)
        self.assertTemplateUsed(response, "student_register.html")

    def test_student_register_valid(self):
        response = self.client.post(
            "/student/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_student)
        self.assertTemplateUsed(response, "index.html")

    def test_student_register_invalid_username(self):
        self.data["username"] = "***"
        response = self.client.post(
            "/student/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["username"][0],
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
        )
        self.assertTemplateUsed(response, "student_register.html")

    def test_student_register_invalid_passwords(self):
        self.data["password"] = "123"
        self.data["confirm_password"] = "1235"
        response = self.client.post(
            "/student/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["confirm_password"][0],
            "Passwords do not match.",
        )
        self.assertTemplateUsed(response, "student_register.html")

    def test_student_register_invalid_age(self):
        self.data["age"] = 5
        response = self.client.post(
            "/student/register", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["age"][0],
            "Age must be between 7 and 80 years.",
        )
        self.assertTemplateUsed(response, "student_register.html")


class TeacherEntryViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        teacher = User.objects.create(username="foo")
        teacher.set_password("123")
        teacher.create_teacher()
        teacher = User.objects.create(username="bar")
        teacher.set_password("123")
        teacher.create_teacher()
        User.objects.create_superuser(username="baz", password="123")
        return super().setUpTestData()

    def setUp(self) -> None:
        cv_file = SimpleUploadedFile("foo.pdf", b"df", "application/pdf")
        demo_file = SimpleUploadedFile("foo.mp4", b"gf", "video/mp4")
        self.data = {
            "first_name": "foo",
            "last_name": "bar",
            "cv": cv_file,
            "demo": demo_file,
        }
        return super().setUp()

    def test_none_user_get(self):
        response = self.client.get("/teacher/1/detsil/entry", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/login")
        self.assertTemplateUsed(response, "signin.html")

    def test_user_not_teacher_get(self):
        self.client.login(username="baz", password="123")
        response = self.client.get("/teacher/1/detsil/entry", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "index.html")

    def test_other_teacher_get(self):
        self.client.login(username="bar", password="123")
        response = self.client.get("/teacher/1/detsil/entry", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "index.html")

    def test_same_teacher_get(self):
        self.client.login(username="foo", password="123")
        response = self.client.get("/teacher/1/detsil/entry", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], Teacher_form)
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")

    def test_other_teacher_post(self):
        self.client.login(username="bar", password="123")
        response = self.client.post(
            "/teacher/1/detsil/entry", data=self.data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")

    def test_same_teacher_post(self):
        self.client.login(username="foo", password="123")
        response = self.client.post(
            "/teacher/1/detsil/entry", data=self.data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTrue(response.wsgi_request.user.techer.activation)
        self.assertEqual(response.wsgi_request.user.techer,
                         Techer.objects.get(pk=1))
        self.assertTemplateUsed(response, "index.html")

    def test_cv_invalid(self):
        self.client.login(username="foo", password="123")
        invalid_cv_file = SimpleUploadedFile("foo.txt", b"df", "text/plain")
        self.data["cv"] = invalid_cv_file
        response = self.client.post(
            "/teacher/1/detsil/entry", data=self.data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["cv"][0], "please upload a pdf file"
        )
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")

    def test_demo_invalid(self):
        self.client.login(username="foo", password="123")
        invalid_cv_file = SimpleUploadedFile("foo.txt", b"df", "text/plain")
        self.data["demo"] = invalid_cv_file
        response = self.client.post(
            "/teacher/1/detsil/entry", data=self.data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].errors["demo"][0], "please upload a mp4 video"
        )
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")


class CourseCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        teacher = User.objects.create(username="foo")
        teacher.set_password("123")
        teacher.create_teacher()
        User.objects.create_superuser(username="baz", password="123")
        return super().setUpTestData()

    def setUp(self) -> None:
        stage = Stage.objects.create(age_start=7, age_end=12, name="foo")
        skill = Skills.objects.create(name="foo")
        self.data = {
            "name": "foo",
            "start_date": datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=5)
            ),
            "stage": stage.id,
            "skill": skill.id,
            "duration": "15w",
            "about": "sjahkld",
        }
        return super().setUp()

    def test_no_user_get(self):
        response = self.client.get("/course/create", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/login")
        self.assertTemplateUsed(response, "signin.html")

    def test_not_teacher_user_get(self):
        self.client.login(username="baz", password="123")
        response = self.client.get("/course/create", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertTemplateUsed(response, "index.html")

    def test_not_accepted_teacher_get(self):
        self.client.login(username="foo", password="123")
        response = self.client.get("/course/create", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, f"/teacher/{(response.wsgi_request.user.id)
                                  }/detsil/entry"
        )
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], Teacher_form)
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")

    def test_accepted_teacher_get(self):
        teacher = Techer.objects.get(pk=1)
        teacher.acceptation = True
        teacher.activation = True
        teacher.save()
        self.client.login(username="foo", password="123")
        response = self.client.get("/course/create", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], Course_Form)
        self.assertTemplateUsed(response, "course_create.html")

    def test_course_post(self):
        teacher = Techer.objects.get(pk=1)
        teacher.acceptation = True
        teacher.activation = True
        teacher.save()
        self.client.login(username="foo", password="123")
        response = self.client.post(
            "/course/create", data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")
        self.assertIn(
            Course.objects.get(
                pk=1), response.wsgi_request.user.techer.course_set.all()
        )
        self.assertTemplateUsed(response, "index.html")


class CourseDeleteViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        teacher = User.objects.create(username="foo")
        teacher.set_password("123")
        teacher.create_teacher()
        stage = Stage.objects.create(age_start=7, age_end=12, name="foo")
        skill = Skills.objects.create(name="foo")
        course = Course.objects.create(
            name='foo',
            start_date=datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=5)
            ),
            stage=stage,
            duration='15',
            about='sjahkld'
        )
        course.skill.add(skill)
        course.save()
        return super().setUpTestData()

    def test_unaccepted_teacher_get(self):
        self.client.login(username='foo', password='123')
        response = self.client.get('/course/1/delete', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/teacher/1/detsil/entry')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], Teacher_form)
        self.assertTemplateUsed(response, "teacher_detsil_entry.html")

    def test_accepted_teacher_get(self):
        teacher = Techer.objects.get(pk=1)
        teacher.acceptation = True
        teacher.activation = True
        teacher.save()
        self.client.login(username='foo', password='123')
        response = self.client.get('/course/1/delete', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('delete_object', response.context)
        self.assertEqual(
            response.context['delete_object'], Course.objects.get(pk=1))
        self.assertTemplateUsed(response, 'delete.html')

    def test_accepted_teacher_post(self):
        teacher = Techer.objects.get(pk=1)
        teacher.acceptation = True
        teacher.activation = True
        teacher.save()
        self.client.login(username='foo', password='123')
        response = self.client.post('/course/1/delete', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        self.assertEqual(Course.objects.count(), 0)
        self.assertTemplateUsed(response, 'index.html')


class CourseListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(7):
            Course.objects.create(
                name='foo',
                start_date=datetime.datetime.date(
                    datetime.datetime.now() + datetime.timedelta(days=5)
                ),
                stage=Stage.objects.create(
                    age_start=7, age_end=12, name="foo"),
                duration='15',
                about='sjahkld'
            )

        return super().setUpTestData()

    def test_pagination(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_paginated', response.context)
        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 5)
        self.assertTemplateUsed(response, 'index.html')

    def test_other_pages(self):
        response = self.client.get(reverse('course_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 2)
        self.assertTemplateUsed(response, 'index.html')


class CourseDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Course.objects.create(
            name='foo',
            start_date=datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=5)
            ),
            stage=Stage.objects.create(
                age_start=7, age_end=12, name="foo"),
            duration='15',
            about='sjahkld'
        )
        return super().setUpTestData()

    def test_get_course(self):
        response = self.client.get(reverse('course_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('course', response.context)
        self.assertEqual(response.context['course'], Course.objects.get(pk=1))
        self.assertTemplateUsed(response, 'course_detail.html')

    def test_get_non_course(self):
        response = self.client.get(reverse('course_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)


class StudentEnrollViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Course.objects.create(
            name='foo',
            start_date=datetime.datetime.date(
                datetime.datetime.now() + datetime.timedelta(days=5)
            ),
            stage=Stage.objects.create(
                age_start=7, age_end=12, name="foo"),
            duration='15',
            about='sjahkld'
        )
        User.objects.create_superuser(username='foo', password='123')
        student = User.objects.create(username='bar', age=8)
        student.set_password('123')
        student.create_student()
        return super().setUpTestData()

    def test_none_user(self):
        response = self.client.get(
            reverse('student_enroll', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login'))

    def test_none_course(self):
        self.client.login(username='bar', password='123')
        response = self.client.get(
            reverse('student_enroll', kwargs={'pk': 2}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_none_student_user(self):
        self.client.login(username='foo', password='123')
        response = self.client.get(
            reverse('student_enroll', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))

    def test_student_user(self):
        self.client.login(username='bar', password='123')
        response = self.client.get(
            reverse('student_enroll', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertIn(response.wsgi_request.user.student,
                      Course.objects.get(pk=1).student.all())


class SectionListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(5):
            Section.objects.create(name=f'{i}')
        return super().setUpTestData()

    def test_list(self):
        response = self.client.get(reverse('section_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sections', response.context)
        self.assertEqual(len(response.context['sections']), 5)
        self.assertIsInstance(response.context['sections'][0], Section)
        self.assertTemplateUsed(response, 'index.html')


class SectionDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Section.objects.create(name='foo')
        return super().setUpTestData()

    def test_get_none_section(self):
        response = self.client.get(
            reverse('section_details', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 404)

    def test_get_section(self):
        response = self.client.get(
            reverse('section_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('section', response.context)
        self.assertEqual(
            response.context['section'], Section.objects.get(pk=1))
        self.assertTemplateUsed(response, 'section_details.html')
class UnitCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        teacher1 = User.objects.create(username='foo')
        teacher1.set_password('123')
        teacher1.create_teacher()
        teacher2 = User.objects.create(username='bar')
        teacher2.set_password('123')
        teacher2.create_teacher()
    def setUp(self) -> None:
        course = Course.objects.create(
            name='foo',
                        start_date=datetime.datetime.date(
                                        datetime.datetime.now() + datetime.timedelta(days=5)
                                                    ),
                                                                stage=Stage.objects.create(
                                                                                age_start=7, age_end=12, name="foo"),
                                                                                            duration='15',
                                                                                                        about='sjahkld'
        )
        course.teacher = Techer.objects.get(pk=1)
        course.save()
        return super().setUpTestData()
    def test_course_teacher(self):
        self.client.login(username='bar', password='123')
        response = self.client.get(reverse('unit_create', kwargs={'course_id':1}))
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse)
