
var map;

function initMap() {
  let local = {lat: 40.9445, lng: -74.0574};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: local
  });
}

function addPlaces(places) {
    for (p of places) {
        console.log(p)
        let local = {lat: parseFloat(p.latitude), lng: parseFloat(p.longitude)};
        let marker = new google.maps.Marker({
          position: local,
          map: map
        });
    }
}


window.onload = function () {

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