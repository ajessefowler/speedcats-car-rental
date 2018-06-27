// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	const today = new Date();
	let menuOut = false;
	let timeOut = false;

	if (document.getElementById('locatebutton')) {
		document.getElementById('locatebutton').addEventListener('click', function() {
			findLocation();
		});
	}

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

	if (document.getElementById('vehiclecontent')) {
		document.getElementById('vehiclecontent').style.top = (document.getElementById('vehicleimage').height + 'px');
	}

	if (document.getElementById('timeselect')) {
		document.getElementById('timeselect').addEventListener('click', function() {
			if (!timeOut) {
				timeOut = true;
				document.getElementById('expandtimecard').style.animation = 'arrowDown .3s ease forwards';
				document.getElementById('timecard').style.animation = 'timeUp .3s ease forwards';
			} else {
				timeOut = false;
				document.getElementById('expandtimecard').style.animation = 'arrowUp .3s ease forwards';
				document.getElementById('timecard').style.animation = 'timeDown .3s ease forwards';
			}
		});

		document.getElementById('donebutton').addEventListener('click', function() {
			const apptDate = document.getElementById('dateinput').value;
			const apptTime = document.getElementById('timeinput').value;
			const meridiem = apptTime >= 12 ? 'PM' : 'AM';

			timeOut = false;
			document.getElementById('timecard').style.animation = 'timeDown .3s ease forwards';
			document.getElementById('timeselecttext').innerHTML = apptDate + ' at ' + apptTime + ' ' + meridiem;
		});
	}

	initLocation();
});