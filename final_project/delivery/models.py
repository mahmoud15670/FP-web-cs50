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
    phone = models.CharField(max_length=11)
    age = models.PositiveSmallIntegerField()
    acceptaiton = models.BooleanField(default=False)
    favoirates = models.CharField(max_length=40)
    section = models.CharField(max_length=20)
    exams = models.CharField(max_length=20)
    cv = models.FileField(upload_to=cv_upload_path)
    demo = models.FileField(upload_to=demo_upload_path)
    group = models.CharField(max_length=20)
    period = models.DateField()
    reting = models.CharField(max_length=5)
    lessons = models.CharField(max_length=20)


class Student(User):
    phone = models.CharField(max_length=11)
    age = models.PositiveSmallIntegerField()
    stage = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    exams = models.CharField(max_length=20)
    group = models.CharField(max_length=20)
    progress = models.PositiveSmallIntegerField(default=0)
    reting = models.CharField(max_length=5)
    certification = models.FileField(upload_to=certificate_upload_path)


class Stage(models.Model):
    techer = models.ForeignKey(to='Techer', on_delete=models.PROTECT, related_name='techers')
    student = models.ForeignKey(to='Student', on_delete=models.PROTECT, related_name='students')
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