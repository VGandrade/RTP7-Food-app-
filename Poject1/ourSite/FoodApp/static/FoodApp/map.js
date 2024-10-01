var map; // Global variable for the map
var service;
var userLocation; // To store the user's current location
var markers = []; // Store all markers
var infoWindows = []; // Store all info windows

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

// Close all open info windows
function closeAllInfoWindows() {
    infoWindows.forEach(function (infoWindow) {
        infoWindow.close();
    });
}

// Function to create markers and add info windows
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
        icon: markerIcon,
        place: place  // Store the entire place object, including place_id
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

    // Store marker and infoWindow for later use
    markers.push({ marker: marker, infoWindow: infoWindow, placeId: place.place_id });
    infoWindows.push(infoWindow);

    let isMouseOverMarker = false;
    let isMouseOverInfoWindow = false;

    // Open InfoWindow when hovering over the marker
    marker.addListener('mouseover', function () {
        isMouseOverMarker = true;
        closeAllInfoWindows();  // Close any open info windows
        infoWindow.open(map, marker);  // Open the new info window
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

// Initialize the map
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

    // Handle search form submission
    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();
        searchRestaurant();
    });

    // Handle dropdown selection
    document.getElementById("restaurant").addEventListener("change", function () {
        let selectedPlaceId = this.value;
        let selected = markers.find(m => m.placeId === selectedPlaceId);  // Find by place_id

        if (selected) {
            closeAllInfoWindows();  // Close all open info windows
            selected.infoWindow.open(map, selected.marker);  // Open the selected info window
            map.setCenter(selected.marker.getPosition());  // Center the map on the selected restaurant
        }
    });
}

// Search for restaurants
function searchRestaurant() {
    console.log("searching");

    var name = document.querySelector('input[name="name"]').value;
    var sortBy = 'rating_high_first';  // Sort by rating high by default
    var distanceFilter = document.querySelector('select[name="distance"]').value;

    var mapOptions = {
        center: new google.maps.LatLng(33.7466, -84.3877),
        zoom: 10
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    service = new google.maps.places.PlacesService(map);

    var request = {
        location: new google.maps.LatLng(33.7490, -84.3880),  // Center search around Atlanta
        radius: '10600',  // Search within a 10km radius
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

            // Sort by rating highest to lowest
            restaurants.sort((a, b) => b.rating - a.rating);

            // Populate the dropdown with the sorted restaurants
            restaurants.forEach(function (restaurant) {
                let option = document.createElement("option");
                option.value = restaurant.place_id;  // Use restaurant place_id for dropdown value
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
