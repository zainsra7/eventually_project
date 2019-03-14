// Comment section (Disqus)

var disqus_config = function () {
    $(document).ready(function () {
        this.page.url = "http://127.0.0.1:8000/eventually/event/";
        this.page.identifier = $('#event-id').val();
    });
};

(function () {
    var d = document, s = d.createElement('script');
    s.src = 'https://eventually-uog.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
})();


// Map (Google)

function initMap() {
    var geocoder = new google.maps.Geocoder;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: { lat: 55.87175, lng: -4.28836 }
    });
    geocodeAddress(geocoder, map);
};

function geocodeAddress(geocoder, map) {
    $(document).ready(function () {
        geocoder.geocode({
            componentRestrictions: {
                country: 'UK',
                postalCode: $('#location').html()
            }
        }, function (results, status) {
            if (status === 'OK') {
                map.setCenter(results[0].geometry.location);
                new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
            }
        });
    });
};


$(document).ready(function () {
    $('.modal').modal();

    // Get request for updated event attendance
    $('#join-button').click(function () {
        var eventid;
        eventid = $(this).attr("data-eventid");

        $.get('/eventually/join/', { event_id: eventid }, function (data) {
            $('#attendee-count').html(data);
            
            // Toggle join/withdraw button
            if ($('#join-button').text() == "Join event") {
                $('#join-button').html('Withdraw'); 
                $('#join-button').addClass('red');
            }
            else {
                $('#join-button').html('Join event');
                $('#join-button').removeClass('red');
            }
        });
    });
});