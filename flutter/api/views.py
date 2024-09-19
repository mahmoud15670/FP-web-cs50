from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

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
    return JsonResponse(data, safe=False)
