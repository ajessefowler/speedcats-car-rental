// Setup location autocomplete and search
function initLocation() {
    const countryRestriction = { componentRestrictions: { country: 'us' }};
    const autocomplete = new google.maps.places.Autocomplete(document.getElementById('locationsearch'), countryRestriction);
   
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
		document.getElementById('locationsearch').blur();
    });
    
    document.getElementById('searchbutton').addEventListener('click', function() {
        const currentLocation = resolveLocation(autocomplete);
    });

    function resolveLocation(element) {
        const place = element.getPlace();
    }
}

// Determine user's current location
function findLocation() {
    if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(resolveCoords, locationError);
	} else {
		alert('Your browser does not support location. Please enter your location.');
	}
}

// Determine the coordinates of the user's current location
function resolveCoords(position) {
	const lat = position.coords.latitude;
	const long = position.coords.longitude;
	const key = 'AIzaSyBTcPqvmsy0xt1IYWSsNnEbipW90i3otLE';
	const url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+ lat + ',' + long + '&key=' + key;
	const request = new XMLHttpRequest();

	request.open('GET', url, true);
	
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			const location = JSON.parse(request.responseText);
		} else {
			console.log('Data error.');
		}
	};

	request.onerror = () => { console.log('Connection error.'); };

	request.send();
}

// Initialize the map, with markers for each store
function initMap() {
    let i;

    for (i = 0; i < locations.length; ++i) {
        const id = (i + 1);
        const addressDisplay = locations[i].address + ', ' + locations[i].city + ', ' + locations[i].state;
        const addressStr = locations[i].address + ',+' + locations[i].city + ',+' + locations[i].state;
        const address = addressStr.replace(/ /g, '+');
        const key = 'AIzaSyBTcPqvmsy0xt1IYWSsNnEbipW90i3otLE';
        const url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ address + '&key=' + key;
        
        const request = new XMLHttpRequest();

	    request.open('GET', url, true);
	
	    request.onload = function() {
		    if (request.status >= 200 && request.status < 400) {
                const location = JSON.parse(request.responseText);
                const coords = location.results[0].geometry.location;
                const marker = new google.maps.Marker({
                    position: coords,
                    map: map
                });
                const vehiclesLink = '/inventory/' + id + '/';

                // Set the select button's link to the selected store
                google.maps.event.addListener(marker, 'click', function() {
                    document.getElementById('select').style.display = 'flex';
                    document.getElementById('selecttext').innerHTML = addressDisplay;
                    document.getElementById('selectlink').onclick = function() {
                        document.location.href = vehiclesLink;
                    }
                });
		    } else {
			    console.log('Data error.');
		    }
	    };

	    request.onerror = () => { console.log('Connection error.'); };

	    request.send();
    }

    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.99, lng: -82.99},
        zoom: 9,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false
    });
}