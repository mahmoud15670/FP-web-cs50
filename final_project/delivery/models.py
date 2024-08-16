from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
def cv_upload_path(techer, file_name):
    return f'delivery/{techer.id}/CV/{file_name}'

def demo_upload_path(techer, file_name):
    return f'delivery/{techer.id}/Demo/{file_name}'

def certificate_upload_path(techer, file_name):
    return f'delivery/{techer.id}/Certificate/{file_name}'

def age_choises():
    return [(i, i) for i in range(7, 81)]