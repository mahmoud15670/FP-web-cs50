from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET'])
def index(request):
    data = [
        {
            'hi':'hi',
            'by':'by'
        },
        {
            'good':'good'
        }
    ]
    return Response(data)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all().order_by('-date_joined')
    serializers = UserSerializer(users, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def register(request):
    data = request.data
    username = data['username']
    password = data['password']
    try:
        user = User.objects.create_user(username=username, password=password)
        return Response(UserSerializer(user, many=False).data)
    except IntegrityError:
        return Response({'warrnin': 'username is already used'})


# {
# "username":"",
# "password":""
# }


@api_view(['post'])
def login_view(request):
    data = request.data
    username = data['username']
    password = data['password']

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'login':f'{user.username} is logged in'})
    return Response({'warrnin': 'username or password is incorect'})

@api_view(['Get'])
def logout_view(request):
    user = request.user.username
    logout(request)
    return Response({'login':f'{user} is logged out'})


@api_view(['GET'])
def getnotes(request):
    notes = Note.objects.all()
    serializers = NoteSerializer(notes, many=True)
    return Response(serializers.data)