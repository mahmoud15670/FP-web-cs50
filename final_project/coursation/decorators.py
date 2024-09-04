from functools import wraps
from django.http import HttpResponseForbidden

def check_student(permission):
    