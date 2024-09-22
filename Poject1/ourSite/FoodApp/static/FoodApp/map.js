document.getElementById('searchButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    const apiKey = "AIzaSyD4oBoretFq5JNK1Zzo2gxk5rSedxmtjiw";  // Replace with your Google API Key
    const url = "https://places.googleapis.com/v1/places:searchNearby";

    const name = document.getElementById('name').value; // Get the restaurant name
    const data = {
        "includedTypes": ["restaurant"],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": 33.7490, // Atlanta latitude
                    "longitude": -84.3880 // Atlanta longitude
                },
                "radius": 500.0
            }
        }
    };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": apiKey,
            "X-Goog-FieldMask": "places.displayName,places.geometry"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Log the API response

        // Clear previous markers if needed
        if (window.markers) {
            window.markers.forEach(marker => marker.setMap(null));
        }
        window.markers = []; // Reset markers array

        // Check if places were found
        if (data.places) {
            data.places.forEach(place => {
                const location = place.geometry.location; // Get the location of the place
                const marker = new google.maps.marker.AdvancedMarkerElement({
                    position: { lat: location.latitude, lng: location.longitude },
                    map: yourMapInstance, // Your Google Maps instance
                    content: `<div>${place.displayName}</div>` // Customize the content as needed
                });
                window.markers.push(marker); // Store the marker
            });
        } else {
            alert("No restaurants found.");
        }
    })
    .catch(error => console.error('Error:', error));
});