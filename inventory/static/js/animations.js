var pickUpTime;
var dropOffTime;

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
		const img = document.getElementById('vehicleimage');
		
		function calculateImgHeight() {
			document.getElementById('vehiclecontent').style.top = (document.getElementById('vehicleimage').height + 'px');
		}

		if (img.complete) {
			calculateImgHeight();
		} else {
			img.addEventListener('load', calculateImgHeight);
		}
	}

	// Add animations and input for time selection
	if (document.getElementById('pickuptimeselect')) {
		initTimeHandler('pickup');
		initTimeHandler('dropoff');
	}

	// Add animations to make reservation page
	if (document.getElementById('reservecontent')) {
		const subelem = document.getElementById('checkoutsub').innerHTML;
		const subtotal = parseInt(subelem.substr(subelem.length - 5));
		const tax = subtotal * 0.07;
		const total = subtotal + tax;
		document.getElementById('checkouttax').innerHTML = 'Tax: $' + tax;
		document.getElementById('checkouttotal').innerHTML = 'Total: $' + total;

		document.getElementById('pickupstore').value = localStorage.getItem('pickup');
		document.getElementById('pickuptime').value = localStorage.getItem('pickuptime');
		document.getElementById('dropoffstore').value = localStorage.getItem('dropoff');
		document.getElementById('dropofftime').value = localStorage.getItem('dropofftime');
		
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

		if (element === 'pickup') {
			pickUpTime = apptDate + ' ' + apptTime;
		} else if (element === 'dropoff') {
			dropOffTime = apptDate + ' ' + apptTime;
		}

		if (pickUpTime && dropOffTime) {
			updateLocalStorageTime();
		}

		document.getElementById(element + 'timecard').style.animation = 'timeDown .3s ease forwards';
		document.getElementById(element + 'timecardtext').innerHTML = apptDate + ' at ' + apptTime + ' ' + meridiem;
		checkStartFormCompletion();
	});

	function updateLocalStorageTime() {
		localStorage.setItem('pickuptime', pickUpTime);
		localStorage.setItem('dropofftime', dropOffTime);
	}
}