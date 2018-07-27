// Add event listeners to done buttons to validate date and time
document.addEventListener('DOMContentLoaded', function(event) {
    if (document.getElementById('pickupdonebutton')) {
        document.getElementById('pickupdonebutton').addEventListener('click', function() {
            const element = 'pickup';
            if (validateTime(element) && validateDate(element)) {
                confirmValidation(element);
            }
        });
    }

    document.getElementById('dropoffdonebutton').addEventListener('click', function() {
        const element = 'dropoff';
        if (validateTime(element) && validateDate(element)) {
            confirmValidation(element);
        }
    });

    function confirmValidation(element) {
        const apptDate = document.getElementById(element + 'dateinput').value;
        const apptTime = document.getElementById(element + 'timeinput').value;
        const formattedDate = formatDate(apptDate);
        const formattedTime = formatTime(apptTime);

        document.getElementById(element + 'timeinput').style.border = 'none';
        document.getElementById(element + 'dateinput').style.border = 'none';
		document.getElementById('timeshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById(element + 'timecard').style.animation = 'timeDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('timeshade').style.display = 'none';
        }, 400);
		document.getElementById(element + 'timetext').innerHTML = formattedDate + ', ' + formattedTime;
		document.getElementById(element + 'timeformat').value = apptDate + ' ' + apptTime;
		checkFormCompletion();
    }

    function formatDate(date) {
        const year = date.substring(0, 4);
        const monthValue = parseInt(date.substring(5, 7));
        const month = getMonth(monthValue);
        const day = date.substring(8, 10);
        const dateString = month + ' ' + day + ', ' + year;

        return dateString;
    }

    function getMonth(value) {
        let month;

        switch (value) {
            case 1:
                month = 'January';
                break;
            case 2:
                month = 'February';
                break;
            case 3:
                month = 'March';
                break;
            case 4:
                month = 'April';
                break;
            case 5:
                month = 'May';
                break;
            case 6:
                month = 'June';
                break;
            case 7:
                month = 'July';
                break;
            case 8:
                month = 'August';
                break;
            case 9:
                month = 'September';
                break;
            case 10:
                month = 'October';
                break;
            case 11:
                month = 'November';
                break;
            case 12:
                month = 'December';
                break;
        }

        return month;
    }
});

function formatTime(time) {
    let hour = parseInt(time.substring(0, 2));
    const mins = time.substring(3);
    const meridiem = hour >= 12 ? 'p.m.' : 'a.m.';

    if (hour > 12) {
        hour -= 12;
    }

    const timeString = hour.toString() + ':' + mins + ' ' + meridiem;
    return timeString;
}

// Ensure that pick up and drop off dates are in the future and consecutive
function validateDate(element) {
    const now = new Date();
    const date = document.getElementById(element + 'dateinput').value;

    if (date) {
        const year = parseInt(date.substring(0, 4));
        const month = parseInt(date.substring(5, 7));
        const day = parseInt(date.substring(8, 10));

        if (element === 'dropoff' && document.getElementById('pickuptimecard')) {
            const pickupDate = document.getElementById('pickupdateinput').value;
            const pickupYear = parseInt(pickupDate.substring(0, 4));
            const pickupMonth = parseInt(pickupDate.substring(5, 7));
            const pickupDay = parseInt(pickupDate.substring(8, 10));

            if (year >= pickupYear && month > pickupMonth) {
                clearAlert(element);
                return true;
            } else if (year >= pickupYear && month === pickupMonth) {
                if (day >= pickupDay) {
                    clearAlert(element);
                    return true;
                } else {
                    document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
                    displayAlert(element, 'Drop off must follow pick up.');
                    return false;
                }
            } else {
                // Check times as well to prevent 0 length reservations
                document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
                displayAlert(element, 'Drop off must follow pick up.');
                return false;
            }
        }
    
        // Add one to now.getMonth because it is 0-indexed
        if (year >= now.getFullYear() && month >= (now.getMonth() + 1)) {
            clearAlert(element);
            return true;
        } else if (year >= now.getFullYear() && month === (now.getMonth() + 1)) {
            if (day >= now.getDate()) {
                clearAlert(element);
                return true;
            } else {
                document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
                displayAlert(element, 'Time must be in the future.');
                return false;
            }
        } else {
            document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
            displayAlert(element, 'Time must be in the future.');
            return false;
        }
    } else {
        document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
        displayAlert(element, 'You must choose a date.');
        return false;
    }

    function compareTimes() {
        const pickupTime = document.getElementById('pickuptimeinput').value;
        const pickupHours = parseInt(pickupTime.substring(0, 2));

        const dropoffTime = document.getElementById('dropofftimeinput').value;
        const dropoffHours = parseInt(dropoffTime.substring(0, 2));

        if (dropoffHours > pickupHours) {
            return true;
        } else {
            return false;
        }
    }
}

// Ensure that pick up and drop off times fall inside store hours
function validateTime(element) {
    const time = document.getElementById(element + 'timeinput').value;
    if (time) {
        const hours = parseInt(time.substring(0, 2));
        const mins = parseInt(time.substring(3, 5));
        if ((hours < 8 || (hours >= 18 && mins > 0))) {
            document.getElementById(element + 'timeinput').style.border = '2px solid #f44336';
            displayAlert(element, 'Time must be between 8 A.M. and 6 P.M.');
            return false;
        } else {
            clearAlert(element);
            return true;
        }
    } else {
        document.getElementById(element + 'timeinput').style.border = '2px solid #f44336';
        displayAlert(element, 'You must choose a time.');
        return false;
    }
}

// Set up the animations for the information selector cards
function initTimeHandler(element) {
	document.getElementById(element + 'time').addEventListener('click', function() {
        document.getElementById('timeshade').style.display = 'block';
        document.getElementById('timeshade').style.animation = 'fadeIn .4s ease forwards';
		document.getElementById(element + 'timecard').style.animation = 'timeUp .4s ease forwards';
	});

	document.getElementById('close' + element + 'time').addEventListener('click', function() {
        document.getElementById('timeshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById(element + 'timecard').style.animation = 'timeDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('timeshade').style.display = 'none';
        }, 400);
    });

    document.getElementById('timeshade').addEventListener('click', function() {
        document.getElementById('timeshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById(element + 'timecard').style.animation = 'timeDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('timeshade').style.display = 'none';
        }, 400);
    });
}


// Display an alert when date or time invalid
function displayAlert(element, message) {
    document.getElementById(element + 'timemessage').style.color = '#FF5722';
    document.getElementById(element + 'timemessage').innerHTML = message;
}

// Clear the alert for the given element
function clearAlert(element) {
    document.getElementById(element + 'timemessage').style.color = '#111';
    document.getElementById(element + 'timemessage').innerHTML = 'Store Hours: 8:00 A.M. to 6:00 P.M.';
}