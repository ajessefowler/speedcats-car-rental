// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	let menuOut = false;

	// Add event listener to find location button
	if (document.getElementById('locatebutton')) {
		initLocation();
		document.getElementById('locatebutton').addEventListener('click', function() {
			findLocation();
		});
	}

	// Slides menu in and out
	document.getElementById('menubutton').addEventListener('click', function() {
		if (!menuOut) {
			menuOut = true;
			document.querySelector('nav').style.animation = 'menuOut .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'chevron_left';
		} else {
			menuOut = false;
			document.querySelector('nav').style.animation = 'menuIn .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'menu';
		}
	});

	// Calculates height of vehicle image to position information
	if (document.getElementById('vehiclecontent')) {
		const img = document.getElementById('vehicleimage');

		if (img.complete) {
			calculateImgHeight();
		} else {
			img.addEventListener('load', calculateImgHeight);
		}

		function calculateImgHeight() {
			const height = document.getElementById('vehicleimage').clientHeight;
			document.getElementById('vehiclecontent').style.top = (height + 'px');
		}
	}

	// Add animations and input for time selection
	if (document.getElementById('mapcontainer')) {
		initTimeHandler('pickup');
		initTimeHandler('dropoff');
	}

	// Show and hide payment form based on location selection
	if (document.getElementById('reservecontent')) {
		document.getElementById('payonline').addEventListener('click', function() {
			document.getElementById('paymentformdiv').style.display = 'block';
		});
		document.getElementById('payinstore').addEventListener('click', function() {
			document.getElementById('paymentformdiv').style.display = 'none';
		});
	}
});

function initTimeHandler(element) {
	document.getElementById(element + 'time').addEventListener('click', function() {
		document.getElementById(element + 'timecard').style.animation = 'timeUp .3s ease forwards';
	});

	document.getElementById('close' + element + 'time').addEventListener('click', function() {
		document.getElementById(element + 'timecard').style.animation = 'timeDown .3s ease forwards';
	});

	document.getElementById(element + 'donebutton').addEventListener('click', function() {
		const apptDate = document.getElementById(element + 'dateinput').value;
		const apptTime = document.getElementById(element + 'timeinput').value;
		const meridiem = apptTime >= 12 ? 'PM' : 'AM';

		document.getElementById(element + 'timecard').style.animation = 'timeDown .3s ease forwards';
		document.getElementById(element + 'time').value = apptDate + ' at ' + apptTime + ' ' + meridiem;
		document.getElementById(element + 'timeformat').value = apptDate + ' ' + apptTime;
		checkStartFormCompletion();
	});
}