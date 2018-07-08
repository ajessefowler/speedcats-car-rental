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

// If all selections have been made, turn the start button orange and activate click handler
function checkStartFormCompletion() {
    const start= document.getElementById('startbutton');

    if (
        (document.getElementById('pickuplocation').value !== 'Tap here to select a location') &&
        (document.getElementById('pickuptime').value !== 'Tap here to select a time') &&
        (document.getElementById('dropofflocation').value !== 'Tap here to select a location') &&
        (document.getElementById('dropofftime').value !== 'Tap here to select a time')
    ) {
        start.style.backgroundColor = '#FF5722';
        start.style.color = '#FFFFFF';
        start.addEventListener('click', function() {
            document.getElementById('selectlocation').submit();
        });
    }
}

function mapOnLoad(request, id, map, addressDisplay, marker, element) {

    // Scroll to top of page to display entire map
    window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth' 
    });

    // Add close animation to close button
    document.getElementById('close' + element).addEventListener('click', function() {
        document.getElementById(element + 'locationcard').style.animation = 'timeDown .3s ease forwards';
    });

    if (request.status >= 200 && request.status < 400) {
        const vehiclesLink = '/inventory/' + id + '/';

        // Set the select button's link to the selected store
        google.maps.event.addListener(marker, 'click', function() {
            document.getElementById(element + 'locationdone').style.color = '#ffffff';
            document.getElementById(element + 'locationtext').innerHTML = addressDisplay;
            
            document.getElementById(element + 'locationdone').addEventListener('click', function() {
                document.getElementById(element + 'locationid').value = id;
                document.getElementById(element + 'location').value = addressDisplay;
                document.getElementById(element + 'locationcard').style.animation = 'timeDown .3s ease forwards';
                document.getElementById(element + 'location').scrollIntoView({
                    behavior: 'smooth'
                });

                checkStartFormCompletion();
            });
        });

    } else {
        console.log('Data error.');
    }
}

// Initialize the map, with markers for each store
function initMap() {
    const key = 'AIzaSyBTcPqvmsy0xt1IYWSsNnEbipW90i3otLE';
    const locations = JSON.parse(localStorage.getItem('locations'));
    let i;

    // Initialize map centered over store locations
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 41.0, lng: -82.99},
        zoom: 6,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false
    });

    for (i = 0; i < locations.length; ++i) {
        const id = (i + 1);
        const addressDisplay = locations[i].address + ', ' + locations[i].city + ', ' + locations[i].state;
        const addressStr = locations[i].address + ',+' + locations[i].city + ',+' + locations[i].state;
        const address = addressStr.replace(/ /g, '+');
        const url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ address + '&key=' + key;
        
        const request = new XMLHttpRequest();

	    request.open('GET', url, true);
	
	    request.onload = function() {
            const location = JSON.parse(request.responseText);
            const coords = location.results[0].geometry.location;
            const marker = new google.maps.Marker({
                position: coords,
                map: map
            });

            document.getElementById('dropofflocation').addEventListener('click', function() {
                mapOnLoad(request, id, map, addressDisplay, marker, 'dropoff');
                document.getElementById('dropofflocationcard').style.animation = 'timeUp .3s ease forwards';
            });

            document.getElementById('pickuplocation').addEventListener('click', function() {
                mapOnLoad(request, id, map, addressDisplay, marker, 'pickup');
                document.getElementById('pickuplocationcard').style.animation = 'timeUp .3s ease forwards';
            });
        };

	    request.onerror = () => { console.log('Connection error.'); };

	    request.send();
    }
}