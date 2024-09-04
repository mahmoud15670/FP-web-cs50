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
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if student_test(request.user):
                return view(request, *args, **kwargs)
            return HttpResponseForbidden('you are not student')
        return _wrapped_view
    return decorator