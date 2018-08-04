// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	let img;
	let element;

	if (document.getElementById('homeimage')) {
		img = document.getElementById('homeimage');
		element = 'homeimage';
	} else {
		img = document.getElementById('vehicleimage');
		element = 'vehicleimage';
	}

	function calculateImgHeight() {
		let height;

		if (window.screen.availWidth < 768) {
			height = document.getElementById(element).clientHeight;
			document.getElementById('vehiclecontent').style.top = (height + 'px');
		} else if (element === 'homeimage' && window.screen.availWidth > 1350) {
			height = document.getElementById(element).clientHeight - 150;
			document.getElementById('vehiclecontent').style.top = (height + 'px');
		} else if (element === 'homeimage') {
			height = document.getElementById(element).clientHeight - 50;
			document.getElementById('vehiclecontent').style.top = (height + 'px');
		}
		
	}

	img.addEventListener('load', calculateImgHeight);
	window.addEventListener('resize', calculateImgHeight)
});