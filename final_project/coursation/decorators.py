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

def teacher_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if teacher_test(request.user):
                return view(request, *args, **kwargs)
            return HttpResponseForbidden('you are not teacher')
        return _wrapped_view
    return decorator

    
def student_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if student_test(request.user):
                return view(request, *args, **kwargs)
            return HttpResponseForbidden('you are not student')
        return _wrapped_view
    return decorator