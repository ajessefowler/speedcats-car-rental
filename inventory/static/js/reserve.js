document.addEventListener('DOMContentLoaded', function(event) {
    // Show and hide payment form based on location selection
	document.getElementById('payonline').addEventListener('click', function() {
		document.getElementById('paymentformdiv').style.display = 'block';
	});
	document.getElementById('payinstore').addEventListener('click', function() {
		document.getElementById('paymentformdiv').style.display = 'none';
	});
});