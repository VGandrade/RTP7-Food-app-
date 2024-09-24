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


}
