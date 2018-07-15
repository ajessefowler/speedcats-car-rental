// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	const img = document.getElementById('vehicleimage');

	function calculateImgHeight() {
		const height = document.getElementById('vehicleimage').clientHeight;
		document.getElementById('vehiclecontent').style.top = (height + 'px');
	}

	img.addEventListener('load', calculateImgHeight);
	window.addEventListener('resize', calculateImgHeight)
});