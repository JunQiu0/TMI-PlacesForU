from django.shortcuts import render
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
# Create your views here.

#Index page 
def index(request):
    return render(request, "placesforu/index.html")

def upload_image(request):
    coords = api.get_landmark("./tmp_image")
    context = {"coords": coords}
    return render(request, "placesforu/coords.html", context)
