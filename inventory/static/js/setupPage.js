// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {

	// Calculates height of vehicle image to position information
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

	// Logic for modification page
	if (document.getElementById('modifyvehicle')) {

	}
});