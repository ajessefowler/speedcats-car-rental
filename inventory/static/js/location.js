document.addEventListener('DOMContentLoaded', function(event) {
    let dropOffSelected;

    // Determine which maps to initialize
    if (document.getElementById('mapcontainer')) {
        initMap('mapcontainer');
    } else {
        if (!document.getElementById('modifylocation')) {
            if (document.getElementById('pickuplocationcard')) {
                initMap('pickup');
            }
        }

        if (document.getElementById('dropofflocationcard')) {
            initMap('dropoff');
        }
    }

    // Control the checking and unchecking of 'drop off at another location' checkbox
    if (document.getElementById('pickuplocationcard')) {
        if (document.getElementById('dropoffdiff')) {
            if (document.getElementById('dropoffdiff').checked) {
                dropOffSelected = true;
            } else {
                dropOffSelected = false;
            }

            document.getElementById('dropoffdiff').addEventListener('click', function(){
                if (!dropOffSelected) {
                    dropOffSelected = true;
                    document.getElementById('dropofflocation').style.display = 'flex';
                    checkFormCompletion();
                } else {
                    dropOffSelected = false;
                    document.getElementById('dropofflocation').style.display = 'none';
                    checkFormCompletion();
                }
            });

            document.getElementById('dropoffdiff').addEventListener('click', function() {
                if (!document.getElementById('dropoffdiff').checked && document.getElementById('pickuplocationid').value != null) {
                    document.getElementById('dropofflocationid').value = document.getElementById('pickuplocationid').value;
                }
            });
        }
    }

    if (document.getElementById('pickuptimecard')) {
        initTimeHandler('pickup');
    }

    if (document.getElementById('dropofftimecard')) {
        initTimeHandler('dropoff');
    }
});

function mapOnLoad(request, id, map, addressDisplay, marker, element) {

    // Add close animation to close button
    document.getElementById('close' + element).addEventListener('click', function() {
        document.getElementById('locationshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById(element + 'locationcard').style.animation = 'mapDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('locationshade').style.display = 'none';
        }, 400);
    });

    document.getElementById('locationshade').addEventListener('click', function() {
        document.getElementById('locationshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById(element + 'locationcard').style.animation = 'mapDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('locationshade').style.display = 'none';
        }, 400);
    });

    // Update page information when a marker is clicked
    if (request.status >= 200 && request.status < 400) {
        const vehiclesLink = '/inventory/' + id + '/';

        // Set the select button's link to the selected store
        google.maps.event.addListener(marker, 'click', function() {
            document.getElementById(element + 'locationdone').style.color = '#111';
            document.getElementById(element + 'locationtext').innerHTML = addressDisplay;
            
            document.getElementById(element + 'locationdone').addEventListener('click', function() {
                if (document.getElementById('pickuplocationcard')) {
                    if (document.getElementById('dropoffdiff')) {
                        if (document.getElementById('dropoffdiff').checked) {
                            document.getElementById(element + 'locationid').value = id;
                        } else {
                            document.getElementById('pickuplocationid').value = id;
                            document.getElementById('dropofflocationid').value = id;
                        }
                    } else {
                        document.getElementById('pickuplocationid').value = id;
                    }
                } else {
                    document.getElementById(element + 'locationid').value = id;
                }
                document.getElementById(element + 'loctext').innerHTML = addressDisplay;
                document.getElementById('locationshade').style.animation = 'fadeOut .4s ease forwards';
                document.getElementById(element + 'locationcard').style.animation = 'mapDown .4s ease forwards';
                setTimeout(function() {
                    document.getElementById('locationshade').style.display = 'none';
                }, 400);

                checkFormCompletion();
            });
        });

    } else {
        console.log('Data error.');
    }
}

// Initialize the map, with markers for each store
function initMap(element) {
    let i;
    let map;
    const key = 'AIzaSyBTcPqvmsy0xt1IYWSsNnEbipW90i3otLE';
    const locations = JSON.parse(localStorage.getItem('locations'));
    const icon = {
        url: markerImage,
        scaledSize: new google.maps.Size(50, 50)
    };

    if (document.getElementById('mapcontainer')) {
        initLocation();
    } else {
        if (document.getElementById('pickuplocationcard')) {
            initLocation('pickup');
        } else if (document.getElementById('dropofflocationcard')) {
            initLocation('dropoff');
        }
    }

    // Initialize map centered over store locations
    if (element !== 'mapcontainer') {
        map = new google.maps.Map(document.getElementById(element + 'map'), {
            center: {lat: 41.0, lng: -82.99},
            zoom: 6,
            zoomControl: true,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            rotateControl: false,
            fullscreenControl: false
        });
    } else {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 41.1, lng: -82.99},
            zoom: 6,
            zoomControl: true,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            rotateControl: false,
            fullscreenControl: false
        });
    }

    // For each location, add a marker on the map
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
                map: map,
                icon: icon
            });

            // Slide location selectors up
            if (document.getElementById('dropofflocation')) {
                document.getElementById('dropofflocation').addEventListener('click', function() {
                    mapOnLoad(request, id, map, addressDisplay, marker, 'dropoff');
                    document.getElementById('locationshade').style.display = 'block';
                    document.getElementById('locationshade').style.animation = 'fadeIn .4s ease forwards';
                    document.getElementById('dropofflocationcard').style.animation = 'mapUp .4s ease forwards';
                });
            }

            if (document.getElementById('pickuplocation')) {
                document.getElementById('pickuplocation').addEventListener('click', function() {
                    mapOnLoad(request, id, map, addressDisplay, marker, 'pickup');
                    document.getElementById('locationshade').style.display = 'block';
                    document.getElementById('locationshade').style.animation = 'fadeIn .4s ease forwards';
                    document.getElementById('pickuplocationcard').style.animation = 'mapUp .4s ease forwards';
                });
            }
        };

	    request.onerror = () => { console.log('Connection error.'); };

	    request.send();
    }

    // Initialize event handlers for find location buttons
    if (document.getElementById('locatebutton')) {
        document.getElementById('locatebutton').addEventListener('click', function() {
            findLocation();
        });
    } else {
        if (document.getElementById('pickuplocatebutton')) {
            document.getElementById('pickuplocatebutton').addEventListener('click', function() {
                findLocation();
            });
        }
        document.getElementById('dropofflocatebutton').addEventListener('click', function() {
            findLocation();
        });
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
        lookAtLocation(lat, long);

        request.open('GET', url, true);
        
        request.onload = function() {
            if (request.status >= 200 && request.status < 400) {
                const location = JSON.parse(request.responseText);
                const city = location.results[0].address_components[3].long_name;
                const state = location.results[0].address_components[5].long_name;
                if (document.getElementById('locationsearch')) {
                    document.getElementById('locationsearch').value = city + ', ' + state;
                } else {
                    document.getElementById('pickuplocationsearch').value = city + ', ' + state;
                    document.getElementById('dropofflocationsearch').value = city + ', ' + state;
                }
            } else {
                console.log('Data error.');
            }
        };

        request.onerror = () => { console.log('Connection error.'); };

        request.send();
    }

    // Alert user when their location cannot be found
    function locationError() {
        alert('Unable to retrieve location.');
    }

    // Setup location autocomplete and search
    function initLocation(element) {
        const countryRestriction = { componentRestrictions: { country: 'us' }};
        let autocomplete;

        // Initialize event handlers for location search and autocomplete
        if (!element) {
            autocomplete = new google.maps.places.Autocomplete(document.getElementById('locationsearch'), countryRestriction);
            
            google.maps.event.addListener(autocomplete, 'place_changed', function() {
                document.getElementById('locationsearch').blur();
            });

            document.getElementById('searchbutton').addEventListener('click', function() {
                const currentLocation = resolveLocation(autocomplete);
            });
        } else {
            if (document.getElementById('pickuplocationsearch')) {
                pickupAutocomplete = new google.maps.places.Autocomplete(document.getElementById('pickuplocationsearch'), countryRestriction);
                
                google.maps.event.addListener(pickupAutocomplete, 'place_changed', function() {
                    document.getElementById('pickuplocationsearch').blur();
                });
            }
            
            dropoffAutocomplete = new google.maps.places.Autocomplete(document.getElementById('dropofflocationsearch'), countryRestriction);

            google.maps.event.addListener(dropoffAutocomplete, 'place_changed', function() {
                document.getElementById('dropfflocationsearch').blur();
            });

            if (document.getElementById('pickupsearchbutton')) {
                document.getElementById('pickupsearchbutton').addEventListener('click', function() {
                    const currentPickUpLocation = resolveLocation(pickupAutocomplete);
                });
            }

            if (document.getElementById('dropoffsearchbutton')) {
                document.getElementById('dropoffsearchbutton').addEventListener('click', function() {
                    const currentDropOffLocation = resolveLocation(dropoffAutocomplete);
                });
            }
        }
        

        // Find coordinates of search location
        function resolveLocation(element) {
            const place = element.getPlace();
            const lat = place.geometry.location.lat();
            const long = place.geometry.location.lng();
            lookAtLocation(lat, long);
        }
    }

    // Set map position to new coordinates and zoom in
    function lookAtLocation(lat, long) {
        const icon = {
            url: markerImageHome,
            scaledSize: new google.maps.Size(50, 50)
        };

        const locationMarker = new google.maps.Marker({
            position: {
                lat: lat,
                lng: long
            },
            map: map,
            icon: icon
        });

        map.setCenter({
            lat: lat,
            lng: long
        });

        map.setZoom(10);
    }
}