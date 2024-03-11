from django.shortcuts import render
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from .models import UploadImageModel
# Create your views here.

#Index page 
def index(request):
    context ={}
    if request.method=="POST":
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image_field")
            obj = UploadImageModel.objects.create(title=name,img=img)
            obj.save()
            print(obj)
    else:
        form=UploadImageForm()
    context['form']=form
    return render(request, "placesforu/index.html", context)

def upload_image(request):
    coords = api.get_landmark("./tmp_image")
    context = {"coords": coords}
    return render(request, "placesforu/coords.html", context)
