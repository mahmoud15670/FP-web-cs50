from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Techer(User):
    phone = models.CharField(max_length=11)
    cv = models.FileField(upload_to='CV', help_text='please upload a PDF file')
    pass