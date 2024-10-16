function initMap() {
  const directionsRenderer = new google.maps.DirectionsRenderer();
  const directionsService = new google.maps.DirectionsService();
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 34,
    center: { lat: 18.030905, lng: 79.542875 },
  });

  directionsRenderer.setMap(map);
  calculateAndDisplayRoute(directionsService, directionsRenderer);
  DRIVING.addEventListener("change", () => {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  const selectedMode = "DRIVING"; //document.getElementById("mode").value;

  directionsService
    .route({
      origin: { lat: 13.6981, lng: -89.1904 },  //13°39'43.0"N 89°15'34.1"W
      destination: { lat: 13.661944, lng: -89.259472 },
      travelMode: google.maps.TravelMode[selectedMode],
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + status));
}

window.alert("The Delivery Agent is on the way");
