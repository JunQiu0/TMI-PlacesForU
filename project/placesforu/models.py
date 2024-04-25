from django.db import models
import pandas as pd

class SearchCount(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    country_iso3 = models.CharField(max_length=3)
    count = models.IntegerField(default=0)

    @classmethod
    def increment_count(self, city, country, country_iso3):
        # Intenta obtener un objeto que coincida con los criterios de consulta, o creará uno nuevo si no existe
        search_count, created = self.objects.get_or_create(city=city, country=country, country_iso3=country_iso3)
        # Incrementa el contador independientemente de si se creó un nuevo objeto o no
        search_count.count += 1
        search_count.save()
    
    def count_per_country():
        '''
        Querying the database to calculate the total searches 
        for a country and the most searched city in each country.
        Returns a DataFrame with 4 columns: country_iso3,
        country, count, most_searched_city. 
        If the table is empty, it returns an empty DataFrame.
        '''
        # Obtener el conteo total por país
        country_counts = (
            SearchCount.objects.values('country_iso3', 'country')
            .annotate(total_count=models.Sum('count'))
        )

        # Crear un dataFrame con los datos del conteo total por pais
        df_country_counts = pd.DataFrame(country_counts, columns=['country_iso3','country','total_count','most_searched_city'])
        # Crear un diccionario para almacenar la ciudad más buscada por país
        most_searched_cities = {}
        
        # Encontrar la ciudad más buscada para cada país
        if not df_country_counts.empty:
            for country_iso3 in df_country_counts['country_iso3']:
                most_searched_city = (
                    SearchCount.objects.filter(country_iso3=country_iso3)
                    .order_by('-count')
                    .first()
                )
                most_searched_cities[country_iso3] = most_searched_city.city if most_searched_city else ""
            # Agregar la información sobre la ciudad más buscada al DataFrame
            df_country_counts['most_searched_city'] = [most_searched_cities[iso3] for iso3 in df_country_counts['country_iso3']]
        return df_country_counts