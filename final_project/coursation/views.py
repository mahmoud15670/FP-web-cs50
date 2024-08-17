from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
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
            'form':Teacher_Form
        })
    form = Teacher_Form(request.POST)
    password = request.POST['password']
    confirm = request.POST['confirm_password']
    if password != confirm:
        return render(request, 'teacher_register.html', {
            'form':form,
            'warning':'password didnot like the confirm'
        })
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'teacher_register.html', {
        'form':form
    })

def teacher_detail_entry(request):
    if request.method != 'POST':
        return render(request, 'teacher_detsil_entry.html', {
            'form':Teacher_detail_form
        })
    user_id = request.POST['user_id']
    teacher = get_object_or_404(Techer, pk=int(user_id))
    
