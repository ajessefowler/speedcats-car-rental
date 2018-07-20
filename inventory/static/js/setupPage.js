// Initialize animations
document.addEventListener('DOMContentLoaded', function(event) {
	const img = document.getElementById('vehicleimage');

	function calculateImgHeight() {
		let height;

		if (window.screen.availWidth < 768) {
			height = document.getElementById('vehicleimage').clientHeight;
		} else {
			height = document.getElementById('vehicleimage').clientHeight - 50;
		}
		document.getElementById('vehiclecontent').style.top = (height + 'px');
	}

	img.addEventListener('load', calculateImgHeight);
	window.addEventListener('resize', calculateImgHeight)
});