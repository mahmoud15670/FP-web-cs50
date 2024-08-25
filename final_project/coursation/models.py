from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def cv_upload_path(techer, file_name):
    return f'coursation/teachers/{techer.id}/CV/{file_name}'

def demo_upload_path(techer, file_name):
    return f'coursation/teachers/{techer.id}/Demo/{file_name}'
def lesson_upload_path(techer, file_name):
    return f'coursation/teachers/{techer.id}/lessons/{file_name}'

def certificate_upload_path(techer, file_name):
    return f'coursation/students/{techer.id}/Certificate/{file_name}'

def age_choises():
    return [(i, i) for i in range(7, 81)]


class User(AbstractUser):
    phone = models.CharField(verbose_name='phone', max_length=11)
    age = models.PositiveSmallIntegerField(null=True)
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT, null=True, help_text='choose the stage you want to learn thim')
    exams = models.CharField(max_length=20, null=True)
    section = models.ForeignKey(to='Section', on_delete=models.PROTECT, null=True, help_text='choose your subject')
    rating = models.CharField(max_length=5, null=True)

class Techer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation = models.BooleanField(default=False)
    acceptation = models.BooleanField(default=False)
    cv = models.FileField(upload_to=cv_upload_path,blank=False, null=True, help_text='upload a cv in pdf format')
    demo = models.FileField(upload_to=demo_upload_path, null=True, help_text='upload a short video in mp4 format to intrduse your self and of your shar7')
    period = models.DateField(null=True)
    lessons = models.CharField(max_length=20, null=True)


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
            return f'age must in range of {self.age_start} and {self.age_end}'
        return {
            'start':self.age_start,
            'end':self.age_end
        }

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
    name = models.CharField(max_length=20, help_text='the name of the group')
    teacher = models.ForeignKey(to='Techer',on_delete=models.PROTECT)
    student = models.ManyToManyField(to='Student', related_name='students')
    leader = models.ForeignKey(to='Student', on_delete=models.PROTECT, null=True)
    lesson = models.ManyToManyField(to='Lessson', null=True)
    count = models.SmallIntegerField(help_text='the number of student that you want to learn thim in this group')

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
    units = models.CharField(max_length=2)
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT)
    skill = models.ManyToManyField(to='Skills')
    duration = models.CharField(max_length=20)
    teacher = models.ForeignKey(to='Techer', on_delete=models.PROTECT)
    student = models.ManyToManyField(to='Student')
    about = models.TextField()
    cirtification = models.FileField(upload_to=certificate_upload_path)
    create_date = models.DateField(auto_now_add=True)
    review = models.IntegerField(default=0,choices={'1':1, '2':2, '3':3, 4:4, 5:5})
class Lessson(models.Model):
    name = models.CharField(max_length=20)
    video = models.FileField(upload_to=lesson_upload_path)
    resource = models.URLField()
    topic = models.TextField()

