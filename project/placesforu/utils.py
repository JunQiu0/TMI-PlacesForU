from .models import SearchCount
import plotly.express as px
import plotly.io as pio
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
import atexit

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

def guardar_html():
    fig_html = get_search_map()
    # Guarda el HTML en un archivo
    with open(settings.BASE_DIR /'placesforu/templates/placesforu/search_map.html', 'w') as file:
        file.write(fig_html)
    print('search html updated')

scheduler = BackgroundScheduler()
scheduler.add_job(guardar_html, trigger=IntervalTrigger(minutes=10))  # Ejecutar cada 10 minuto para actualizar estadisticas de busqueda
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
