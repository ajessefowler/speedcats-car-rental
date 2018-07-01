// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	const today = new Date();
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
		document.getElementById('vehiclecontent').style.top = (document.getElementById('vehicleimage').height + 'px');
	}

	// Add animations and input for time selection
	if (document.getElementById('pickuptimeselect')) {
		initTimeHandler('pickup');
		initTimeHandler('dropoff');
	}

	// Add animations to make reservation page
	if (document.getElementById('reservecontent')) {
		document.getElementById('paymentlocationcontinue').addEventListener('click', function() {
			console.log(document.querySelector('input[name="paymentlocation"]:checked').value);
		});
	}
});

function initTimeHandler(element) {
	document.getElementById(element + 'timeselect').addEventListener('click', function() {
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
		document.getElementById(element + 'timecardtext').innerHTML = apptDate + ' at ' + apptTime + ' ' + meridiem;
		checkStartFormCompletion();
	});
}