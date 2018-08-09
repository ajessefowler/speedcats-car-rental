// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	let img;
	let element;

	// Determine which elements need to be resized
	if (document.getElementById('homeimage')) {
		img = document.getElementById('homeimage');
		element = 'homeimage';
	} else {
		img = document.getElementById('vehicleimage');
		element = 'vehicleimage';
	}

	// Find height of image and set top of content to that height
	function calculateImgHeight() {
		let height;
		let contentDiv;

		if (document.getElementById('vehiclecontent')) {
			contentDiv = 'vehiclecontent';
		} else {
			contentDiv = 'vehiclehomecontent';
		}

		// Vary height based on screen size
		if (window.screen.availWidth < 768) {
			height = document.getElementById(element).clientHeight;
			document.getElementById(contentDiv).style.top = (height + 'px');
		} else if (element === 'homeimage' && window.screen.availWidth > 1350) {
			height = document.getElementById(element).clientHeight - 150;
			document.getElementById(contentDiv).style.top = (height + 'px');
		} else if (element === 'homeimage') {
			height = document.getElementById(element).clientHeight - 50;
			document.getElementById(contentDiv).style.top = (height + 'px');
		}
		
	}

	// Calculate image height on load and on resize
	img.addEventListener('load', calculateImgHeight);
	window.addEventListener('resize', calculateImgHeight)
});