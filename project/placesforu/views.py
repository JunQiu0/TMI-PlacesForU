from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from imageupload.models import UploadImageModel
# Create your views here.

#Index page 
def index(request):
    context ={}
    if request.method=="POST":
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            #name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image_field")
            obj = UploadImageModel.objects.create(title="imagen",img=img)
            obj.save()
            print(img)
            return upload_image(request, f"images/{img}")
    else:
        form=UploadImageForm()
    context['form']=form
    return render(request, "placesforu/index.html", context)

def upload_image(request, path):
    img_data = api.get_landmark(path)
    #img_data = None
    coords = None
    if img_data:
        coords = (img_data["latitude"], img_data["longitude"])
    #coords = (2222, -1111) # Para pruebas
    context = {"coords": coords}
    return render(request, "placesforu/coords.html", context)
