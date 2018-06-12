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
			document.querySelector('nav').style.animation = 'menuOut .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'chevron_left';
		} else {
			menuOut = false;
			document.querySelector('nav').style.animation = 'menuIn .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'menu';
		}
	});

	initLocation();
});