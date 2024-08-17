from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def cv_upload_path(techer, file_name):
    return f'delivery/{techer.id}/CV/{file_name}'

def demo_upload_path(techer, file_name):
    return f'delivery/{techer.id}/Demo/{file_name}'

def certificate_upload_path(techer, file_name):
    return f'delivery/{techer.id}/Certificate/{file_name}'

def age_choises():
    return [(i, i) for i in range(7, 81)]


class Techer(User):
    activation = models.BooleanField(default=False )
    phone = models.CharField(max_length=11)
    age = models.PositiveSmallIntegerField(null=True)
    acceptaiton = models.BooleanField(default=False)
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT, null=True, blank=True)
    section = models.CharField(max_length=20, null=True, blank=True)
    exams = models.CharField(max_length=20, null=True, blank=True)
    cv = models.FileField(upload_to=cv_upload_path, null=True, blank=True)
    demo = models.FileField(upload_to=demo_upload_path, null=True, blank=True)
    groub = models.CharField(max_length=20, null=True, blank=True)
    period = models.DateField(null=True, blank=True)
    reting = models.CharField(max_length=5, null=True, blank=True)
    lessons = models.CharField(max_length=20, null=True, blank=True)


class Student(User):
    phone = models.CharField(max_length=11)
    age = models.PositiveSmallIntegerField()
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT)
    section = models.CharField(max_length=20)
    exams = models.CharField(max_length=20)
    group = models.CharField(max_length=20)
    progress = models.PositiveSmallIntegerField(default=0)
    reting = models.CharField(max_length=5)
    certification = models.FileField(upload_to=certificate_upload_path)


class Stage(models.Model):
    age_start = models.PositiveSmallIntegerField(choices=age_choises)
    age_end = models.PositiveSmallIntegerField(choices=age_choises)
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