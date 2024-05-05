from django.shortcuts import render
from django.shortcuts import redirect
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from imageupload.models import UploadImageModel
from django.conf import settings
from .models import SearchCount
from . import utils
import csv, re, os
import numpy as np
from django.contrib.sessions.backends.db import SessionStore

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
    try:
        with open(settings.BASE_DIR /'placesforu/templates/placesforu/search_map.html', 'r', encoding='utf-8') as file:
            fig_html = file.read() 
    except FileNotFoundError as e:
        print(e)
        utils.guardar_html()
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
    nearest_cities = []
    cities = []
    city_names = []

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
        
    if coords:
        cities, nearest_cities, city_names = get_airports(coords)

    context = {"coords": coords, "path": img_url, "cities": cities,
                "nearest_cities": nearest_cities, "city_names": city_names,
                "upload_image_url": upload_image_store_link}
    context['API_KEY']= settings.API_KEY
    return render(request, "placesforu/coords.html", context)

def get_airports(coords):
    A = []
    cities = []
    city_names = []

    print(coords)

    with open(os.path.join(os.path.dirname(__file__), './static/airports.csv'), 'r', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            coordenadas = re.findall(r"[-+]?\d*\.\d+|\d+", fila["location"])
            A.append((float(coordenadas[1]), float(coordenadas[0])))
            cities.append(fila["code"])
            city_names.append(re.sub('[^a-zA-Z]', ' ', fila["name"]))

    A = np.array(A)
    cities = np.array(cities)
    leftbottom = np.array(coords)
    distances = np.linalg.norm(A - leftbottom, axis=1)
    min_indices = np.where(distances < 1.0)

    return cities[min_indices].tolist(), cities.tolist(), city_names