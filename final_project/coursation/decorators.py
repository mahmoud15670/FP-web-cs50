from functools import wraps

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *


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
                return HttpResponseRedirect(reverse("index"))
            return HttpResponseRedirect(reverse("login"))

        return _wrapped_view

    return decorator


def accepted_teacher():
    def decorator(view):
        @teacher_access_only()
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.techer.activation and request.user.techer.acceptation:
                return view(request, *args, **kwargs)
            return HttpResponseRedirect(
                reverse("teacher_detail_entry", args=(request.user.id,))
            )

        return _wrapped_view

    return decorator


def student_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if student_test(request.user):
                    return view(request, *args, **kwargs)
                return HttpResponseRedirect(reverse("index"))
            return HttpResponseRedirect(reverse("login"))

        return _wrapped_view

    return decorator


def course_select():
    def decorator(view):
        @accepted_teacher()
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            course = get_object_or_404(Course, pk=kwargs["course_id"])
            if course.teacher.id != request.user.techer.id:
                return HttpResponseRedirect(
                    reverse("course_detail", kwargs={"pk": kwargs["course_id"]})
                )
            return view(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def unit_select():
    def decorator(view):
        @accepted_teacher()
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            unit = get_object_or_404(Unit, pk=kwargs["unit_id"])
            if unit.course.teacher.id != request.user.techer.id:
                return HttpResponseRedirect(
                    reverse("unit_detail", kwargs={"pk": kwargs["unit_id"]})
                )
            return view(request, *args, **kwargs)

        return _wrapped_view

    return decorator
