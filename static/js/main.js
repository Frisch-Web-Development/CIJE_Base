
var map;    // the Google map
var y = 40.739915, x = -73.999459;    // coordinates of where we are located, default Manhattan

function initMap() {
  let latitude = y; let longitude = x;
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
        y = latitude; x = longitude;
        map.setCenter({lat: y, lng: x});
    });
  }
  let local = {lat: y, lng: x};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: local
  });
}

function addPlaces(places) {
    for (let p of places) {
        console.log(p)

        let currentImage = {
            url: "/static/icons/" + p.type.toLowerCase() + ".png",
            scaledSize: new google.maps.Size(32, 32),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(0, 0),
            labelOrigin: new google.maps.Point(16, 38)
        }

        let local = {lat: parseFloat(p.latitude), lng: parseFloat(p.longitude)};
        let marker = new google.maps.Marker({
            position: local,
            title: p.name,
            icon: currentImage,
            map: map
        });
        let infowindow = new google.maps.InfoWindow({
            content: p.other
        });
        marker.setLabel(p.type);
        marker.addListener('click', function() {
            infowindow.open(map, marker);
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


    $('#exampleModal').on('show.bs.modal', function(event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var recipient = button.data('whatever') // Extract info from data-* attributes
          // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
          // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
          var modal = $(this)
          modal.find('.modal-title').text('New message to ' + recipient)
          modal.find('.modal-body input').val(recipient)
    })

};
