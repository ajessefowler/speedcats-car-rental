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
             } else {
                 resetStartButton();
             }
        } else {
            setStartButton();
        }
    }

    function setStartButton() {
        const start = document.getElementById('startbutton');
        start.style.backgroundColor = '#FF5722';
        start.style.color = '#FFFFFF';
        start.onclick = submitForm;
    }

    function resetStartButton() {
        const start = document.getElementById('startbutton');
        start.style.backgroundColor = 'rgb(126, 126, 126)';
        start.style.color = '#696969';
        start.onclick = null;
    }

    function submitForm() {
        document.getElementById('selectlocation').submit();
    }
}