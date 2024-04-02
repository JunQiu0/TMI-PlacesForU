// Initialize and add the map
let map;

async function initMap() {
  
  const coords = JSON.parse(document.getElementById('coords').textContent);
  const position = { lat: coords[0], lng: coords[1]};
  
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  // The map
  map = new Map(document.getElementById("map"), {
    zoom: 18,
    center: position,
    mapId: "MAP_ID",
  });

  // The marker
  const marker = new AdvancedMarkerView({
    map: map,
    position: position,
    title: "Location",
  });

  // The geocoder
  const geocoder = new google.maps.Geocoder();

  geocoder
    .geocode({ location: position })
    .then((response) => {
      if (response.results[0]) {
        //document.getElementById('address').textContent = response.results[1].formatted_address;

      }
    })
    .catch((e) => window.alert("Geocoder failed due to: " + e));
}

initMap();


