var map; // Global variable for the map
var service;



function createMarker(place) {
    // Check if geometry exists
    if (!place.geometry || !place.geometry.location) {
        console.log("Place has no geometry information.");
        return;
    }

    // Create a marker on the map at the restaurant's location
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    console.log("Marker created for: " + place.name + " at " + place.geometry.location);
}

function initMap() {
    var atlanta = { lat: 33.7490, lng: -84.3880 };

    // Initialize the map centered at Atlanta
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: atlanta,
    });

    // Add an event listener for the form submission
    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault(); // Prevent the default form submission
        searchRestaurant(); // Call the search function
    });
}

function searchRestaurant() {
    console.log("searching");

    var name = document.querySelector('input[name="name"]').value;
    console.log("Name: " + name);
    var mapOptions = {
        center: new google.maps.LatLng(33.7466, -84.3877),
        zoom:10
    }
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    service = new google.maps.places.PlacesService(map);

    var request ={
        location: new google.maps.LatLng(33.7490, -84.3880),  // Center search around Atlanta
        radius: '5000',  // Search within a 5km radius
        keyword: name,  // User input for restaurant name
        type: 'restaurant'  // Limit results to restaurants
    }
    service.nearbySearch(request, function(results, status)
    {
        if(status === google.maps.places.PlacesServiceStatus.OK)
        {
            for(var i = 0; i<results.length; i++) {
                console.log("Result " + (i + 1) + ": " + results[i].name);
                console.log("Location: " + results[i].geometry.location.lat() + ", " + results[i].geometry.location.lng());
                createMarker(results[i]);
            }
            map.setCenter(results[0].geometry.location);
        } else {
            console.log("No results found or error occurred. Status: " + status);
            alert("No restaurant found with the name '" + name + "'. Please try again.");
        }
    })

    function createMarker(place, index) {
        var marker = new google.maps.Marker({
            map: map,
            position: place.geometry.location,
            title: place.name  // Set the marker's title (shows on hover by default)
        });

        var googleMapsLink = 'https://www.google.com/maps/place/?q=place_id:' + place.place_id;

        var infoWindow = new google.maps.InfoWindow({
            content: '<div id="infowindow-content"><strong>' + place.name + '</strong><br>' +
                     'Rating: ' + (place.rating ? place.rating : 'No rating available') + '<br>' +
                     'Address: ' + place.vicinity + '<br>' +
                     '<a href="' + googleMapsLink + '" target="_blank">View on Google Maps</a></div>'
        });

        let isMouseOverInfoWindow = false;

        // Add listeners to the InfoWindow content for mouseover and mouseout
        google.maps.event.addListener(infoWindow, 'domready', function() {
            var infoWindowContent = document.getElementById('infowindow-content');
            infoWindowContent.addEventListener('mouseover', function() {
                isMouseOverInfoWindow = true;
            });
            infoWindowContent.addEventListener('mouseout', function() {
                isMouseOverInfoWindow = false;
                setTimeout(function() {
                    if (!isMouseOverMarker && !isMouseOverInfoWindow) {
                        infoWindow.close();
                    }
                }, 100);
            });
        });

        let isMouseOverMarker = false;

        // Open InfoWindow when hovering over the marker
        marker.addListener('mouseover', function() {
            isMouseOverMarker = true;
            infoWindow.open(map, marker);
        });

        // Close InfoWindow only if both mouse is not over the marker and not over the InfoWindow
        marker.addListener('mouseout', function() {
            isMouseOverMarker = false;
            setTimeout(function() {
                if (!isMouseOverMarker && !isMouseOverInfoWindow) {
                    infoWindow.close();
                }
            }, 100);
        });

        // Bind hover event to the restaurant list item too
        var listItem = document.getElementById('restaurant-' + index);
        listItem.addEventListener('mouseover', function() {
            isMouseOverMarker = true;
            infoWindow.open(map, marker);
        });
        listItem.addEventListener('mouseout', function() {
            isMouseOverMarker = false;
            setTimeout(function() {
                if (!isMouseOverMarker && !isMouseOverInfoWindow) {
                    infoWindow.close();
                }
            }, 100);
        });
    }

    function createRestaurantListItem(place, index) {
        // Create a list item in the HTML for the restaurant
        var restaurantList = document.getElementById('restaurant-list');
        var listItem = document.createElement('li');
        listItem.id = 'restaurant-' + index;
        listItem.innerHTML = place.name + ' - ' + place.vicinity;
        restaurantList.appendChild(listItem);
    }



}
