from django.forms import BaseModelForm
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *
# بسم الله الرحمن الرحيم
def index(request):
    if request.user.is_authenticated:
        try:
            if request.user.techer in Techer.objects.all():
                s = ContentFile(request.user.techer.cv)
                return render(request, 'teacher.html', {
                    'teacher':request.user.techer,
                    's':s
                })
        except ObjectDoesNotExist:
            try:
                if request.user.student in Student.objects.all():
                    return render(request, 'student.html')
            except ObjectDoesNotExist:
                return render(request, 'index.html')
    else:
        stage_list = Stage.objects.all()
        sections = Section.objects.all()
        skills = Skills.objects.all()
        courses = Course.objects.all()
        return render(request, 'index.html', {
            'stage_list':stage_list,
            'sections':sections,
            'skills':skills,
            'courses':courses
        })

class Stage_List(generic.ListView):
    model = Stage
    template_name = 'index.html'
    context_object_name = 'stage_list'

def login_view(request):
    if request.method != 'POST':
        return render(request, 'signin.html')
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'signin.html', {
            'massage':'the user name or  password is incorrect'
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def teacher_register(request):
    if request.method != 'POST':
        return render(request, 'teacher_register.html', {
            'form':User_Form
        })
    user_form = User_Form(request.POST)
    password = request.POST['password']
    confirm = request.POST['confirm_password']
    if password != confirm:
        return render(request, 'teacher_register.html', {
            'form':user_form,
            'warning':'password didnot like the confirm'
        })
    if user_form.is_valid():
        user = user_form.save()
        teacher = Techer.objects.create(user=user, id=user.id)
        teacher.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'teacher_register.html', {
        'form':user_form
    })

def student_register(request):
    if request.method != 'POST':
        return render(request, 'student_register.html', {
            'form':User_Student_Form
        })
    user_form = User_Student_Form(request.POST)
    password = request.POST['password']
    confirm = request.POST['confirm_password']
    if password != confirm:
        return render(request, 'student_register.html', {
            'form':user_form,
            'warning':'password didnot like the confirm'
        })
    if user_form.is_valid():
        user = user_form.save()
        for stage in Stage.objects.all():
            if stage.age()['start'] <= user.age and  user.age <= stage.age()['end']:
                user.stage = stage
                user.save()
        student = Student.objects.create(user=user, id=user.id)
        student.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'student_register.html', {
        'form':user_form
    })


class Teacher_detail_entry(generic.UpdateView):
    model = Techer
    form_class = Teacher_form
    template_name = 'teacher_detsil_entry.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args: str, **kwargs) -> HttpResponse:
        if self.request.user.id != int(kwargs['pk']):
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.id != int(self.kwargs['pk']):
            return super().form_invalid(form)
        teacher = form.save(commit=False)
        teacher.user.first_name = form.cleaned_data['first_name']
        teacher.user.last_name = form.cleaned_data['last_name']
        teacher.user.save()
        teacher.activation = True
        return super().form_valid(form)


class Group_creation(generic.CreateView):
    model = Groub
    form_class = Group_Form
    template_name = 'group_creation.html'
    success_url = reverse_lazy('index')

    
    def form_valid(self, form):
        group = form.save(commit=False)
        if self.request.user.techer.activation and self.request.user.techer.acceptation:
            group.teacher = self.request.user.techer
            group.save()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse('index'))


class Group_detail_view(generic.DetailView):
    model = Groub
    template_name = 'group_details.html'
    context_object_name = 'group'


class Course_create_view(generic.CreateView):
    model = Course
    form_class = Course_Form
    template_name = 'course_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        course = form.save(commit=False)
        if self.request.user.techer.activation and self.request.user.techer.acceptation:
            course.teacher = self.request.user.techer
            course.save()
            return super().form_valid(form)
        return HttpResponseRedirect(reverse('index'))


class Course_detail_view(generic.DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'


@login_required(login_url='login')
def student_enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.student.add(request.user.student)
    return HttpResponseRedirect(reverse('index'))


class Section_list_view(generic.ListView):
    model = Section
    template_name = 'index.html'
    context_object_name = 'sections'


class Section_details_view(generic.DetailView):
    model = Section
    template_name = 'section_details.html'
    context_object_name = 'section'
