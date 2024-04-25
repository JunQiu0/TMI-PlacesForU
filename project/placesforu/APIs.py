from google.cloud import vision
from geopy.geocoders import Nominatim
import pycountry

def get_landmark(image_path, link = False):
    '''Given a route to a local image or a link to a
    remote image this method returns the location of
    the image (as a dict) or None otherwise. The server 
    running must have a token for the google vision API.
    
    Structure of the dict:
    {
        "latitude": float,
        "longitude": float,
        "landmark": "string" (name of the landmark),
        "score": "float" (confidence of the landmark detection)
    }
    '''
    coord = None    #Default coords
    path = image_path

    # Use google vision API to find location
    client = vision.ImageAnnotatorClient()

    image = None
    if link:
        image = vision.Image()
        image.source.image_uri = path
    else:
        with open(path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    # Build dict with the info
    # Coords, landmark name
    if landmarks:
        coord = {
            "latitude": landmarks[0].locations[0].lat_lng.latitude,
            "longitude": landmarks[0].locations[0].lat_lng.longitude,
            "landmark": landmarks[0].description,
            "score": f"{landmarks[0].score:.2f}"
        }

    return coord

def get_country_city(latitude, longitude):
    '''
    Given the latitude and longitude, returns the country, 
    its ISO3 code, and the city according to OSM through Nominatim. 
    In case of failure, it returns none. 
    '''
    try:
        geolocalizador = Nominatim(user_agent="placesforu")
        location = geolocalizador.reverse((latitude, longitude), exactly_one=True, language='es')
        country_eng = geolocalizador.reverse((latitude, longitude), exactly_one=True, language='en').raw['address'].get('country', '')
        address = location.raw['address']
        city = address.get('city', '')
        country = address.get('country', '')
        country_iso3 = pycountry.countries.lookup(country_eng).alpha_3
    except Exception as e:
        country_iso3 = None
        country = None
        city = None

    return city, country, country_iso3


