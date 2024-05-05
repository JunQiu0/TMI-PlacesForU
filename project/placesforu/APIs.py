from google.cloud import vision
from geopy.geocoders import Nominatim
from django.http import HttpResponse
import pycountry
import json, requests, time

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

def get_flights(request):
    data = json.loads(request.body)
    flights = []
    found = False
    i = 0
    api_response = None
    #print(request.session["amadeus_token"])
    #for i in range(len(data["possible_cities"])):
    request.session["amadeus_token"] = generate_token()
    while not found and i < len(data['possible_cities']):
        headers = {
            'Authorization': f'Bearer {request.session["amadeus_token"]}'
        }
        print(data['possible_cities'][i])
        print(request.session["amadeus_token"])
        #url = f"https://api.travelpayouts.com/v1/prices/cheap?origin={data['origin']}&destination={data['possible_cities'][i]}&depart_date={data['date']}&token=07baab25c478d0d653be62a8f1688a2c&currency=eur"
        url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={data['origin']}&destinationLocationCode={data['possible_cities'][i]}&departureDate={data['date']}&adults=1&nonStop=true&max=6"
        api_response = requests.get(url,headers=headers)  # Realizar la petición GET
        flight_data = json.loads(api_response.text)
        print(api_response.text)
        if api_response.status_code == 401 and (flight_data["errors"][0]["code"] == 38191 or flight_data["errors"][0]["code"] == 38192): #It is necessary to renew the flight API token
            request.session["amadeus_token"] = generate_token()
            i = i - 1
        elif api_response.status_code == 200: #Call was successful
            if flight_data['meta']['count'] > 0: #If a flight has been found
                for flight in flight_data['data']:
                    flights.append(flight)
                #found = True
        i = i + 1
        time.sleep(0.6)
    json_data = json.dumps(flights) #Return empty array if no flights have been found
    response = HttpResponse(json_data, content_type='application/json')
    return response

def generate_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "client_credentials",
        "client_id": "MmFF23SecmaOa9YXt0BjxVTX2UCU8KuH",
        "client_secret": "BUHseG29xUnTg3Cv"
    }
    response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token", data=payload, headers=headers)
    return json.loads(response.text)['access_token']