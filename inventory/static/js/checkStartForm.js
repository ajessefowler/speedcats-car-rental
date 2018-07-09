// If all selections have been made, turn the start button orange and activate click handler
function checkFormCompletion() {
    if (
        (document.getElementById('pickuploctext').innerHTML !== 'Tap here to select a location') &&
        (document.getElementById('pickuptimetext').innerHTML !== 'Tap here to select a time') &&
        (document.getElementById('dropofftimetext').innerHTML !== 'Tap here to select a time')
    ) {
        if (document.getElementById('dropoffdiff').checked) {
             if (document.getElementById('dropoffloctext').innerHTML !== 'Tap here to select a location') {
                 setStartButton();
             }
        } else {
            setStartButton();
        }
    }

    function setStartButton() {
        const start = document.getElementById('startbutton');
        start.style.backgroundColor = '#FF5722';
        start.style.color = '#FFFFFF';
        start.addEventListener('click', function() {
            document.getElementById('selectlocation').submit();
        });
    }
}