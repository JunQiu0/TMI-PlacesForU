from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Index page 
def index(request):
    return HttpResponse("Hello, django!")