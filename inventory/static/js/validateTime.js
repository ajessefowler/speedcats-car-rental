// Add event listeners to done buttons to validate date and time
document.addEventListener('DOMContentLoaded', function(event) {
    document.getElementById('pickupdonebutton').addEventListener('click', function() {
        const element = 'pickup';
        if (validateTime(element) && validateDate(element)) {
            confirmValidation(element);
        }
    });
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
		document.getElementById(element + 'timecard').style.animation = 'timeDown .3s ease forwards';
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
});

// Ensure that pick up and drop off dates are in the future and consecutive
function validateDate(element) {
    const now = new Date();
    const date = document.getElementById(element + 'dateinput').value;
    const year = parseInt(date.substring(0, 4));
    const month = parseInt(date.substring(5, 7));
    const day = parseInt(date.substring(8, 10));

    if (element === 'dropoff') {
        const pickupDate = document.getElementById('pickupdateinput').value;
        const pickupYear = parseInt(pickupDate.substring(0, 4));
        const pickupMonth = parseInt(pickupDate.substring(5, 7));
        const pickupDay = parseInt(pickupDate.substring(8, 10));

        if (year < pickupYear || month < pickupMonth || day < pickupDay) {
            // Check times as well to prevent 0 length reservations
            document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
            return false;
        } else {
            return true;
        }
    }
    
    // Add one to now.getMonth because it is 0-indexed
    if (year !== now.getFullYear() || month < (now.getMonth() + 1) || day < (now.getDate())) {
        document.getElementById(element + 'dateinput').style.border = '2px solid #f44336';
        return false;
    } else {
        return true;
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
    const hours = parseInt(time.substring(0, 2));
    const mins = parseInt(time.substring(3, 5));
    if (hours < 8 || (hours >= 18 && mins > 0)) {
        document.getElementById(element + 'timeinput').style.border = '2px solid #f44336';
        return false;
    } else {
        return true;
    }
}

function initTimeHandler(element) {
	document.getElementById(element + 'time').addEventListener('click', function() {
		document.getElementById(element + 'timecard').style.animation = 'timeUp .3s ease forwards';
	});

	document.getElementById('close' + element + 'time').addEventListener('click', function() {
		document.getElementById(element + 'timecard').style.animation = 'timeDown .3s ease forwards';
	});
}