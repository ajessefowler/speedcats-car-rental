// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	let menuOut = false;

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

	initLocation();
});