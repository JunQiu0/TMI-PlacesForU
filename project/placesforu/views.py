from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#Index page 
def index(request):
    return render(request, "placesforu/index.html")