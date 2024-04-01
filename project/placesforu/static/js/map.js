// Initialize and add the map
let map;

async function initMap(latitud, longitud) {
  const position = { lat: latitud, lng: longitud };

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
}

