from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from imageupload.models import UploadImageModel
from django.conf import settings
from .models import SearchCount
from . import utils
import os

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
                # Store imagen path
                obj = UploadImageModel(title="imagen", img=img)
                obj.save()
                print(f"Imagen guardada: {obj.img.url}")
                # Para prueba ./placesforu/test_resources/test.png
                return upload_image(request, f"{obj.img.path}", False)
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
    # Lee el contenido de la plantilla
    with open(settings.BASE_DIR /'placesforu/templates/placesforu/search_map.html', 'r', encoding='utf-8') as file:
        fig_html = file.read() 
    context['fig_html']=fig_html

    return render(request, "placesforu/index.html", context)

def upload_image(request, img_url, isURL):
    img_data = None
    try:
        img_data = api.get_landmark(img_url, link=isURL)
    except Exception as e:
        print(f"Error: {e}")
        img_data = None
    #img_obj.delete()
    # Create the context with the image data returned by the API
    coords = None
    if img_data:
        coords = (img_data["latitude"], img_data["longitude"])
        city, country, country_iso3= api.get_country_city(img_data["latitude"], img_data["longitude"])
        if city and country_iso3 and country:
            SearchCount.increment_count(city, country, country_iso3)
    if not isURL:
        server_base_url = request.build_absolute_uri('/media/images')
        upload_image_store_link = f"{server_base_url}/{os.path.basename(img_url)}"
    else:
        upload_image_store_link = img_url
    context = {"coords": coords, "upload_image_url": upload_image_store_link}
    context['API_KEY']= settings.API_KEY
    return render(request, "placesforu/coords.html", context)

