from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import placesforu.APIs as api
from django.template import Context
from .forms import UploadImageForm
from imageupload.models import UploadImageModel
from django.conf import settings
from .models import SearchCount
# Create your views here.
import plotly.express as px
import plotly.io as pio
import pandas as pd


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
    fig_html = get_search_map()
    context['form']=form
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
    context = {"coords": coords}
    context['API_KEY']= settings.API_KEY
    return render(request, "placesforu/coords.html", context)

# Auxiliary function
def get_search_map():
    df_country_counts = SearchCount.count_per_country()
    # Caso de base de dato vacio
    if df_country_counts.empty:
        df_country_counts = pd.DataFrame({'country_iso3': ['ESP'], 'country': ['España'], 'total_count': [1], 'most_searched_city': ['Madrid']})

    fig = px.choropleth(df_country_counts, locations='country_iso3',
                        locationmode="ISO-3",
                        color="total_count",
                        hover_name="country",
                        hover_data={"most_searched_city":True, "total_count":True,'country_iso3':False},
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection='orthographic',
                        labels={'total_count': 'Número total de búsqueda', 
                                'most_searched_city': 'Ciudad más buscada',},
                        title='Search history')
    # Poner transparencia en todos los lados
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )
    # No mostrar leyenda de escala
    fig.update(layout_coloraxis_showscale=False)
    # Centralizar el titulo
    fig.update_layout(title={'text': 'Search history', 'x': 0.5})
    #Devuelve un html
    return pio.to_html(fig, full_html=False)

    