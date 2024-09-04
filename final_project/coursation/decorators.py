from functools import wraps
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect

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
            if request.user.is_authenticated:
                if teacher_test(request.user):
                    return view(request, *args, **kwargs)
                return HttpResponseRedirect(reverse('index'))
            return HttpResponseRedirect(reverse('login'))
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