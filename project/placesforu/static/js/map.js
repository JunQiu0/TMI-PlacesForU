// Initialize and add the map
let map;

async function initMap() {
  
  const coords = JSON.parse(document.getElementById('coords').textContent);
  if (coords){
    // Arranque
    const API_KEY = JSON.parse(document.getElementById('API_KEY').textContent);
    (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
    ({key: API_KEY, v: "beta"});
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
}

initMap();


