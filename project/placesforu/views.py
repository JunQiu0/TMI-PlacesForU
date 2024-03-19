from django.shortcuts import render
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
# Create your views here.

#Index page 
def index(request):
    src_map = api.get_map_src(40.45285938607549,-3.7336615037034977)
    context = {"src_map": src_map}
    return render(request, "placesforu/index.html", context)

def upload_image(request):
    coords = api.get_landmark("./tmp_image")
    context = {"coords": coords}
    return render(request, "placesforu/coords.html", context)
