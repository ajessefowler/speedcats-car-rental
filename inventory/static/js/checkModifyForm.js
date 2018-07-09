// If all selections have been made, turn the start button orange and activate click handler
function checkFormCompletion() {
    if (
        (document.getElementById('pickuptimetext').innerHTML !== 'Tap here to select a time') &&
        (document.getElementById('dropofftimetext').innerHTML !== 'Tap here to select a time')
    ) {
        if (document.getElementById('dropoffdiff').checked) {
             if (document.getElementById('dropoffloctext').innerHTML !== 'Tap here to select a location') {
                 setDoneButton();
             }
        } else {
            setDoneButton();
        }
    }

    function setDoneButton() {
        const modify = document.getElementById('modifybutton');
        modify.style.backgroundColor = '#FF5722';
        modify.style.color = '#FFFFFF';
        modify.addEventListener('click', function() {
            document.getElementById('selectlocation').submit();
        });
    }
}