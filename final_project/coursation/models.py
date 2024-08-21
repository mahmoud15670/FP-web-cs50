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
    stage = models.ForeignKey(to='Stage', on_delete=models.PROTECT, null=True)
    exams = models.CharField(max_length=20, null=True)
    section = models.ForeignKey(to='Section', on_delete=models.PROTECT, null=True)
    rating = models.CharField(max_length=5, null=True)

class Techer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation = models.BooleanField(default=False)
    acceptation = models.BooleanField(default=False)
    cv = models.FileField(upload_to=cv_upload_path, null=True)
    demo = models.FileField(upload_to=demo_upload_path, null=True)
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

class Groub(models.Model):
    name = models.CharField(max_length=20)
    teacher = models.ForeignKey(to='Techer',on_delete=models.PROTECT)
    student = models.ManyToManyField(to='Student', related_name='students')
    leader = models.ForeignKey(to='Student', on_delete=models.PROTECT, null=True)
    lesson = models.CharField(max_length=20, null=True)
    count = models.SmallIntegerField()

    def is_avilable(self):
        if self.count == self.student.count():
            return False
        return True
    def avilable_count(self):
        student_count = self.student.count()
        return self.count - student_count

class Lessson(models.Model):
    name = models.CharField(max_length=20)
    video = models.FileField(upload_to=lesson_upload_path)
    resource = models.URLField()
    topic = models.TextField()
    
