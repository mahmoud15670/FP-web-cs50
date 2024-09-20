from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User (User):
    pass 

class Note(models.Model):
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body[0:50]
    
    class Meta:
        ordering = ['-updated']