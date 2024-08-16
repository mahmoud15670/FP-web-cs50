from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method != 'POST':
        return render(request, 'signin.html')
    username = request.POST['username']
    password = request.POST['password']
    