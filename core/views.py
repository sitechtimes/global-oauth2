from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("<h1>Hello world</h1>")


def login(request):
    return HttpResponse('<input type="hidden" name="next" value="{{ next }}" />')
