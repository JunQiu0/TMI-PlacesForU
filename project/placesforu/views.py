from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from imageupload.models import UploadImageModel
from django.conf import settings
# Create your views here.

#Index page 
def index(request):
    context ={}
    if request.method=="POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("image_field")
            img_url = form.cleaned_data.get("image_url")
            # Replace spaces with underscores because the image name will be used as a path
            if img:
                img.name = img.name.replace(' ', '_')
                obj = UploadImageModel(title="imagen", img=img)
                obj.save()
                print(f"Imagen guardada: {obj.img.url}")
                # Para prueba ./placesforu/test_resources/test.png
                return upload_image(request, f"{obj.img.url}", False)
            else:
                print(f"URL: {img_url}")
                return upload_image(request, img_url, True)
    elif request.method=="GET":
        if "image_url" in request.GET: # GET request with image URL
            print(f"URL: {request.GET.get('image_url')}")
            img_url = request.GET.get("image_url")
            return upload_image(request, img_url, True)
        else: # Normal GET request
            form = UploadImageForm()
    context['form']=form
    return render(request, "placesforu/index.html", context)

def upload_image(request, path, isURL):
    img_data = None
    try:
        img_data = api.get_landmark(path, link=isURL)
    except Exception as e:
        print(f"Error: {e}")
        img_data = None

    # Create the context with the image data returned by the API
    coords = None
    if img_data:
        coords = (img_data["latitude"], img_data["longitude"])
    #coords = (40.45285938607549, -3.7336615037034977) # Para pruebas
    context = {"coords": coords, "path": path}
    context['API_KEY']= settings.API_KEY
    return render(request, "placesforu/coords.html", context)
