from functools import wraps
from django.http import HttpResponseForbidden

def teacher_test(user):
    if user.is_teacher:
        return True
    return False

def student_test(user):
    if user.is_student:
        return True
    return False

def check_student():
    def decorator(view):
        