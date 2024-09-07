import datetime
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractUser


def cv_upload_path(techer, file_name):
    return f"teachers/{techer.id}/CV/{file_name}"


def demo_upload_path(techer, file_name):
    return f"teachers/{techer.id}/Demo/{file_name}"


def lesson_upload_path(techer, file_name):
    return f"teachers/{techer.id}/lessons/{file_name}"


def course_photo_path(course, file_name):
    return Course.upload_path(course) + f"photos/{file_name}"


def certificate_upload_path(techer, file_name):
    return f"students/{techer.id}/Certificate/{file_name}"


def unit_video_upload_path(unit, file_name):

    return Lesson.upload_path(unit) + f"/{unit.id}/Video/{file_name}"


def unit_read_upload_path(unit, file_name):

    return Lesson.upload_path(unit) + f"{unit.id}/read/{file_name}"


def age_choises():
    return [(i, i) for i in range(7, 81)]


class User(AbstractUser):
    phone = models.CharField(verbose_name="phone", max_length=11)
    age = models.PositiveSmallIntegerField(null=True)
    stage = models.ForeignKey(
        to="Stage",
        on_delete=models.PROTECT,
        null=True,
        help_text="choose the stage you want to learn thim",
    )
    exams = models.CharField(max_length=20, null=True)
    section = models.ForeignKey(
        to="Section",
        on_delete=models.PROTECT,
        null=True,
        help_text="choose your subject",
    )
    rating = models.CharField(max_length=5, null=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def create_tracher(self):
        self.is_teacher = True
        self.save()
        teacher = Techer.objects.create(user=self, id=self.id)
        teacher.save()


class Techer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation = models.BooleanField(default=False)
    acceptation = models.BooleanField(default=False)
    cv = models.FileField(
        upload_to=cv_upload_path,
        blank=False,
        null=True,
        help_text="upload a cv in pdf format",
    )
    demo = models.FileField(
        upload_to=demo_upload_path,
        null=True,
        help_text="upload a short video in mp4 format to intrduse your self and of your shar7",
    )

    def __str__(self) -> str:
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.PositiveSmallIntegerField(default=0)
    certification = models.FileField(upload_to=certificate_upload_path)

    def __str__(self) -> str:
        return self.user.username


class Stage(models.Model):
    age_start = models.PositiveSmallIntegerField(choices=age_choises())
    age_end = models.PositiveSmallIntegerField(choices=age_choises())
    name = models.CharField(max_length=20)

    def age(self):
        if self.age_start >= self.age_end:
            return f"age must in range of {self.age_start} and {self.age_end}"
        return {"start": self.age_start, "end": self.age_end}

    def __str__(self) -> str:
        return self.name


class Exam(models.Model):
    date = models.DateTimeField(auto_now_add=False, auto_created=False)
    total = models.SmallIntegerField()
    degree = models.SmallIntegerField()
    duration = models.TimeField(auto_now_add=False, auto_created=False)
    question = models.TextField()
    answer = models.TextField()


class Section(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Groub(models.Model):
    name = models.CharField(max_length=20, help_text="the name of the group")
    teacher = models.ForeignKey(to="Techer", on_delete=models.PROTECT)
    student = models.ManyToManyField(to="Student", related_name="students")
    leader = models.ForeignKey(to="Student", on_delete=models.PROTECT, null=True)
    lesson = models.ManyToManyField(to="Lesson", null=True)
    count = models.SmallIntegerField(
        help_text="the number of student that you want to learn thim in this group"
    )

    def is_avilable(self):
        if self.count == self.student.count():
            return False
        return True

    def avilable_count(self):
        student_count = self.student.count()
        return self.count - student_count


class Course(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    stage = models.ForeignKey(to="Stage", on_delete=models.PROTECT)
    skill = models.ManyToManyField(to="Skills")
    photo = models.FileField(upload_to=course_photo_path, null=True)
    duration = models.CharField(max_length=20)
    teacher = models.ForeignKey(to="Techer", on_delete=models.PROTECT, null=True)
    student = models.ManyToManyField(to="Student", null=True)
    about = models.TextField()
    cirtification = models.FileField(upload_to=certificate_upload_path, null=True)
    create_date = models.DateField(auto_now_add=True)
    review = models.IntegerField(
        default=0, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True
    )

    def is_started(self):
        if self.start_date > datetime.datetime.now().date():
            return False
        return True

    def exam_count(self):
        num = []
        for unit in self.unit_set.all():
            for lesson in unit.lesson_set.all():
                num.append(lesson.exam.count())
        return sum(num)

    def upload_path(self):
        return f"teachers/{self.teacher.id}/Courses/{self.id}/"


class Unit(models.Model):
    name = models.CharField(max_length=20)
    goal = models.TextField()
    course = models.ForeignKey(to="Course", on_delete=models.CASCADE)

    def get_video_count(self):
        num = 0
        for lesson in self.lesson_set.all():
            if lesson.video:
                num = num + 1
        return num

    def get_read_count(self):
        num = 0
        for lesson in self.lesson_set.all():
            if lesson.read:
                num = num + 1
        return num


class Lesson(models.Model):
    unit = models.ForeignKey(to="Unit", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    topic = models.TextField()
    video = models.FileField(upload_to=unit_video_upload_path, blank=True)
    read = models.FileField(upload_to=unit_read_upload_path, blank=True)
    exam = models.ManyToManyField(to="Exam", null=True)

    def upload_path(self):
        return f"teachers/{self.unit.course.teacher.id}/Courses/{self.unit.course.id}/Units/{self.unit.id}/Lessons"
