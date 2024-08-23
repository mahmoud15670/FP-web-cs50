from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try:
            if request.user.techer in Techer.objects.all():
                return render(request, 'teacher.html')
        except ObjectDoesNotExist:
            try:
                if request.user.student in Student.objects.all():
                    return render(request, 'student.html')
            except ObjectDoesNotExist:
                return render(request, 'index.html')
    else:
        stage_list = Stage.objects.all()
        sections = Section.objects.all()
        return render(request, 'index.html', {
            'stage_list':stage_list,
            'sections':sections
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



    def form_valid(self, form):
        print(self.request.user.id)
        print(self.pk_url_kwarg)
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
            raise ValidationError('you are not active please complete yor profile')



class Group_detail_view(generic.DetailView):
    model = Groub
    template_name = 'group_details.html'
    context_object_name = 'group'

@login_required(login_url='login')
def student_enroll(request, pk):
    group = get_object_or_404(Groub, pk=pk)
    group.student.add(request.user.student)
    return HttpResponseRedirect(reverse('index'))


class Section_list_view(generic.ListView):
    model = Section
    template_name = 'index.html'
    context_object_name = 'sections'


class Section_details_view(generic.DetailView):
    model = Section
    template_name = 'section_details.html'
    context_object_name = 'section'
