from google.cloud import vision

def get_landmark(image_path):
    '''Given a route to a local image returns the location 
    of the image (as a dict) or None otherwise. The server 
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
