var map; // Global variable for the map
var service;
var userLocation; // To store the user's current location

// Function to calculate distance between two points using the Haversine formula
function calculateDistance(loc1, loc2) {
    var R = 6371; // Radius of the Earth in km
    var dLat = (loc2.lat() - loc1.lat()) * Math.PI / 180;
    var dLng = (loc2.lng() - loc1.lng()) * Math.PI / 180;
    var a =
        0.5 - Math.cos(dLat) / 2 +
        Math.cos(loc1.lat() * Math.PI / 180) * Math.cos(loc2.lat() * Math.PI / 180) *
        (1 - Math.cos(dLng)) / 2;

    return R * 2 * Math.asin(Math.sqrt(a));
}

function createMarker(place, isClosest = false) {
    // Check if geometry exists
    if (!place.geometry || !place.geometry.location) {
        console.log("Place has no geometry information.");
        return;
    }

    // Create a marker with a different color for the closest restaurant
    var markerIcon = isClosest
        ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';

    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        icon: markerIcon // Change icon for the closest restaurant
    });

    var googleMapsLink = `https://www.google.com/maps/place/?q=place_id:${place.place_id}`;

    // Create an InfoWindow with the restaurant details
    var infoWindowContent = `
        <div id="infowindow-content">
            <strong>${place.name}</strong><br>
            Address: ${place.vicinity || 'Address not available'}<br>
            Rating: ${place.rating ? place.rating + ' / 5' : 'No rating available'}<br>
            <a href="${googleMapsLink}" target="_blank">View on Google Maps</a>
        </div>
    `;

    var infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent
    });

    let isMouseOverMarker = false;
    let isMouseOverInfoWindow = false;

    // Open InfoWindow when hovering over the marker
    marker.addListener('mouseover', function () {
        isMouseOverMarker = true;
        infoWindow.open(map, marker);
    });

    // Close InfoWindow when mouse leaves both marker and InfoWindow
    marker.addListener('mouseout', function () {
        isMouseOverMarker = false;
        setTimeout(function () {
            if (!isMouseOverMarker && !isMouseOverInfoWindow) {
                infoWindow.close();
            }
        }, 100);
    });

    // Add mouseover/mouseout for InfoWindow
    google.maps.event.addListener(infoWindow, 'domready', function () {
        var infoWindowElement = document.getElementById('infowindow-content');
        infoWindowElement.addEventListener('mouseover', function () {
            isMouseOverInfoWindow = true;
        });
        infoWindowElement.addEventListener('mouseout', function () {
            isMouseOverInfoWindow = false;
            setTimeout(function () {
                if (!isMouseOverMarker && !isMouseOverInfoWindow) {
                    infoWindow.close();
                }
            }, 100);
        });
    });
}

function initMap() {
    var atlanta = { lat: 33.7490, lng: -84.3880 };

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: atlanta,
    });

    // Get user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            map.setCenter(userLocation);
            createMarker({ geometry: { location: userLocation }, name: 'Your Location' });
        });
    }

    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();
        searchRestaurant();
    });
}

function searchRestaurant() {
    console.log("searching");

    var name = document.querySelector('input[name="name"]').value;
    var sortBy = document.querySelector('select[name="sort"]').value;
    var distanceFilter = document.querySelector('select[name="distance"]').value;

    console.log("Name: " + name);
    console.log("Sort By: " + sortBy);
    console.log("Distance Filter: " + distanceFilter);

    var mapOptions = {
        center: new google.maps.LatLng(33.7466, -84.3877),
        zoom: 10
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    service = new google.maps.places.PlacesService(map);

    var request = {
        location: new google.maps.LatLng(33.7490, -84.3880),  // Center search around Atlanta
        radius: '5000',  // Search within a 5km radius
        keyword: name,
        type: 'restaurant'
    };

    service.nearbySearch(request, function (results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            let restaurants = [];
            let restaurantDropdown = document.getElementById("restaurant");  // Get dropdown element

            // Clear existing dropdown options
            restaurantDropdown.innerHTML = `<option value="" selected disabled>Select a restaurant</option>`;

            for (var i = 0; i < results.length; i++) {
                var distance = calculateDistance(new google.maps.LatLng(userLocation), results[i].geometry.location);
                
                // Add distance to the restaurant object
                results[i].distance = distance;
                restaurants.push(results[i]);
            }

            // Sort the results based on the selected filters
            if (sortBy === 'rating_high_first') {
                restaurants.sort((a, b) => b.rating - a.rating);
            } else if (sortBy === 'rating_low_first') {
                restaurants.sort((a, b) => a.rating - b.rating);
            }

            if (distanceFilter === 'close_to_far') {
                restaurants.sort((a, b) => a.distance - b.distance);
            } else if (distanceFilter === 'far_to_close') {
                restaurants.sort((a, b) => b.distance - a.distance);
            }

            // Populate the dropdown with the sorted restaurants
            restaurants.forEach(function (restaurant) {
                let option = document.createElement("option");
                option.value = restaurant.name;  // You can use restaurant ID if available
                option.text = `${restaurant.name} - ${restaurant.vicinity} (Rating: ${restaurant.rating})`;
                restaurantDropdown.appendChild(option);  // Append the new option to the dropdown
            });

            // After sorting, update the markers on the map
            let closestRestaurant = null;
            let minDistance = Infinity;

            for (let i = 0; i < restaurants.length; i++) {
                var distance = restaurants[i].distance;

                // Check if this restaurant is the closest one
                if (distance < minDistance) {
                    minDistance = distance;
                    closestRestaurant = restaurants[i];
                }

                createMarker(restaurants[i]);
            }

            // Mark the closest restaurant with a different color
            if (closestRestaurant) {
                createMarker(closestRestaurant, true);
            }

            map.setCenter(restaurants[0].geometry.location);
        } else {
            console.log("No results found or error occurred. Status: " + status);
            alert("No restaurant found with the name '" + name + "'. Please try again.");
        }
    });
}
