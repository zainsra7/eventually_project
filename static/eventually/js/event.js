// Comment section

var disqus_config = function () {
    this.page.url = "http://127.0.0.1:8000/eventually/event/";  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = "hashCode"; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};

(function () {
    var d = document, s = d.createElement('script');
    s.src = 'https://eventually-uog.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
})();


// Map

function initMap() {
    var geocoder = new google.maps.Geocoder;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: { lat: 55.87175, lng: -4.28836 }
    });
    geocodeAddress(geocoder, map);
};

function geocodeAddress(geocoder, map) {
    geocoder.geocode({
        componentRestrictions: {
            country: 'UK',
            postalCode: 'G128RZ'
        }
    }, function (results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        } else {
            window.alert('Geocode was not successful for the following reason: ' +
                status);
        }
    });
}


$(document).ready(function () {
    $('.modal').modal();
});