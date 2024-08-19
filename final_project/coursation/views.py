from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.http import HttpResponseRedirect

from .forms import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

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
        teacher = Techer.objects.create(user=user)
        teacher.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'teacher_register.html', {
        'form':user_form,
        'warning':'enter correct data'
    })

def student_register(request):
    if request.method != 'POST':
        return render(request, 'student_register.html', {
            'form':User_Form
        })
    user_form = User_Form(request.POST)
    password = request.POST['password']
    confirm = request.POST['confirm_password']
    if password != confirm:
        return render(request, 'student_register.html', {
            'form':user_form,
            'warning':'password didnot like the confirm'
        })
    if user_form.is_valid():
        user = user_form.save()
        student = Student.objects.create(user=user)
        student.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'student_register.html', {
        'form':user_form,
        'warning':'enter correct data'
    })


def teacher_detail_entry(requset, pk):
    if requset != 'POST':
        return render(requset, 'teacher_detsil_entry.html', {
            'user_form':User_detail_form,
            'teacher_form':Teacher_form
        })
    user_form = User_Form(requset.POST)
    teacher_form = Teacher_form(requset.POST)

    if user_form.is_valid() and teacher_form.is_valid():
        teacher = get_object_or_404(Techer, pk=pk)
        print(teacher)        
# class Teacher_detail_entry(generic.UpdateView):
#     model = Techer
#     form_class = [User_detail_form, Teacher_form]
#     template_name = 'teacher_detsil_entry.html'
#     success_url = reverse_lazy('index')
    
#     def form_valid(self, form):
#         teacher = form.save(commit=False)
#         teacher.activation = True
#         teacher.save()
#         return super().form_valid(form)

    
