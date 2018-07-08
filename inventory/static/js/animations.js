var pickUpTime;
var dropOffTime;

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

	// Add animations to make reservation page
	if (document.getElementById('reservecontent')) {
		const msInOneDay = 86400000;
		const reservePickUp = localStorage.getItem('pickuptime');
		const pickUpTime = formatTime(reservePickUp);
		const reserveDropOff = localStorage.getItem('dropofftime');
		const dropOffTime = formatTime(reserveDropOff);
		const length = (((dropOffTime - pickUpTime) / msInOneDay) + 1);

		const subelem = document.getElementById('checkoutsub').value;
		const subtotal = Number(parseFloat(subelem.substr(subelem.length - 5)) * length).toFixed(2);
		const tax = Number(parseFloat(subtotal) * 0.07).toFixed(2);
		const total = Number(parseFloat(subtotal) + parseFloat(tax)).toFixed(2);
		document.getElementById('checkoutsub').value = 'Subtotal: $' + subtotal;
		document.getElementById('checkouttax').value = 'Tax: $' + tax;
		document.getElementById('checkouttotal').value = 'Total: $' + total;

		document.getElementById('pickupstore').value = localStorage.getItem('pickup');
		document.getElementById('pickuptime').value = localStorage.getItem('pickuptime');
		document.getElementById('dropoffstore').value = localStorage.getItem('dropoff');
		document.getElementById('dropofftime').value = localStorage.getItem('dropofftime');

		// Show and hide payment form based on location selection
		document.getElementById('payonline').addEventListener('click', function() {
			document.getElementById('paymentformdiv').style.display = 'block';
		});
		document.getElementById('payinstore').addEventListener('click', function() {
			document.getElementById('paymentformdiv').style.display = 'none';
		});
	}

	function formatTime(timeStr) {
		const year = timeStr.substr(0,4);
		const month = timeStr.substr(5,2);
		const day = timeStr.substr(8,2);
		const hour = timeStr.substr(11,2);
		const min = timeStr.substr(14,2);
		const date = new Date(year, month, day, hour, min);
		return date;
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