
var map;

function initMap() {
  let latitude = 40.739915; let longitude = -73.999459;
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
        map.setCenter({lat: latitude, lng: longitude});
    });
  }
  let local = {lat: latitude, lng: longitude};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: local
  });
}

function addPlaces(places) {
    for (let p of places) {
        console.log(p)
        let local = {lat: parseFloat(p.latitude), lng: parseFloat(p.longitude)};
        let marker = new google.maps.Marker({
          position: local,
          map: map
        });
    }
}


window.onload = function() {

    $.ajax({
        method: "GET",
        url: "/getlocations",
        data: "application/json"
    }).done(function(data) {
        console.log(data);
        initMap();
        addPlaces(data);
    });

};