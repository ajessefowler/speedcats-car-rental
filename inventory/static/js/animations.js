// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
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
			document.querySelector('header').style.animation = 'menuOut .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'expand_less';
		} else {
			menuOut = false;
			document.querySelector('header').style.animation = 'menuIn .3s ease forwards';
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
				document.getElementById('timecard').style.animation = 'timeUp .4s ease forwards';
			}
		});

		document.getElementById('donebutton').addEventListener('click', function() {
			timeOut = false;
			document.getElementById('timecard').style.animation = 'timeDown .4s ease forwards';
		});
	}

	initLocation();
});