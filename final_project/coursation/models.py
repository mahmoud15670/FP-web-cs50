from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
def cv_upload_path(techer, file_name):
    return f'coursation/teachers/{techer.id}/CV/{file_name}'

def demo_upload_path(techer, file_name):
    return f'coursation/teachers/{techer.id}/Demo/{file_name}'

def certificate_upload_path(techer, file_name):
    return f'coursation/students/{techer.id}/Certificate/{file_name}'

def age_choises():
    return [(i, i) for i in range(7, 81)]


class Techer(AbstractUser):
    activation = models.BooleanField(default=False )
    phone = models.CharField(max_length=11)
    age = models.PositiveSmallIntegerField(null=True)
    acceptaiton = models.BooleanField(default=False)
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT, null=True)
    section = models.ForeignKey(to='Section', on_delete=models.PROTECT, null=True)
    exams = models.CharField(max_length=20, null=True)
    cv = models.FileField(upload_to=cv_upload_path, null=True)
    demo = models.FileField(upload_to=demo_upload_path, null=True)
    groub = models.CharField(max_length=20, null=True)
    period = models.DateField(null=True)
    reting = models.CharField(max_length=5, null=True)
    lessons = models.CharField(max_length=20, null=True)


class Student(Techer):
    progress = models.PositiveSmallIntegerField(default=0)
    certification = models.FileField(upload_to=certificate_upload_path)


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

class Groub(models.Model):
    teacher = models.ManyToManyField(to='Techer')
    student = models.ManyToManyField(to='Student')
    leader = models.ForeignKey(to='Student', on_delete=models.PROTECT)
    lesson = models.CharField(max_length=20)
    count = models.SmallIntegerField()
    
