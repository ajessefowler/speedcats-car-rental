// Validation regular expressions found here: https://www.w3resource.com/javascript/form/credit-card-validation.php
document.addEventListener('DOMContentLoaded', function(event) {
    let cardValidated = false;

    // Check if card number is valid
    document.getElementById('cardnumber').addEventListener('blur', function() {
        const number = document.getElementById('cardnumber').value;

        if (getTypeOfCard(number, false)) {
            cardValidated = true;
            document.getElementById('cardtype').value = getTypeOfCard(number, true);
            removeErrorBorder('cardnumber');
        } else {
            cardValidated = false;
            document.getElementById('cardnumber').placeholder = 'Invalid Card Number';
            addErrorBorder('cardnumber');
            clearLogoColor();
        }
    });

    // Set payment type to instore if pay in store button is clicked
    document.getElementById('payinstore').addEventListener('click', function() {
        document.getElementById('cardtype').value = 'i';
    });

    document.getElementById('payonline').addEventListener('click', function() {
        // If card number hasn't been entered, set payment type to undefined
        if (document.getElementById('cardnumber').value.length === 0) {
            document.getElementById('cardtype').value = '';
        }

        // If card has been eneterd, set payment type to type of card
        if (document.getElementById('cardtype').value !== '') {
            const number = document.getElementById('cardnumber').value;
            if (getTypeOfCard(number, false)) {
                const paymentType = getTypeOfCard(number, false);
                document.getElementById('cardtype').value = paymentType;
            }
        }
    });

    // If form content is not valid, prevent committing the reservation
    document.getElementById('reservecontinuebutton').addEventListener('click', function(event) {
        if (document.getElementById('cardtype').value !== 'i' && !validateForm()) {
            event.preventDefault();
        }
    });

    // Determine the type of card entered
    function getTypeOfCard(number, setStyle) {
        if (validateVisa(number)) {
            document.getElementById('visalogo').classList.add('activelogo');
            return 'v';
        } else if (validateMastercard(number)) {
            document.getElementById('mastercardlogo').classList.add('activelogo');
            return 'm';
        } else if (validateDiscover(number)) {
            document.getElementById('discoverlogo').classList.add('activelogo');
            return 'd';
        } else if (validateAmex(number)) {
            document.getElementById('amexlogo').classList.add('activelogo');
            return 'a';
        } else {
            return false;
        }
    }

    // Ensure payment form has been filled out correctly and card has been validated
    function validateForm() {
        checkLength('cardname', 2, true);
        checkLength('securitycode', 2, true);
        checkLength('zipcode', 4, true);
        if (!cardValidated || !formCompleted()) {
            return false;
        } else {
            return true;
        }
    }

    // Ensure payment form has been filled out correctly
    function formCompleted() {
        if (checkLength('cardname', 2, false) &&
            checkLength('securitycode', 2, false) &&
            checkLength('zipcode', 4, false)) {
                return true;
        } else {
            return false;
        }
    }

    function checkLength(elementID, minLength, setStyle) {
        if (document.getElementById(elementID).value.length > minLength) {
            if (setStyle) {
                removeErrorBorder(elementID);
            }
            return true;
        } else {
            if (setStyle) {
                addErrorBorder(elementID);
            }
            return false;
        }
    }
});

// Check if card type is Visa
function validateVisa(cardNumber) {
    const cardValidator = /^(?:4[0-9]{12}(?:[0-9]{3})?)$/;

    if (cardNumber.match(cardValidator)) {
        return true;
    } else {
        return false;
    }
}

// Check if card type is Mastercard
function validateMastercard(cardNumber) {
    const cardValidator = /^(?:5[1-5][0-9]{14})$/;

    if (cardNumber.match(cardValidator)) {
        return true;
    } else {
        return false;
    }
}

// Check if card type is Discover
function validateDiscover(cardNumber) {
    const cardValidator = /^(?:6(?:011|5[0-9][0-9])[0-9]{12})$/;

    if (cardNumber.match(cardValidator)) {
        return true;
    } else {
        return false;
    }
}

// Check if card type is American Express
function validateAmex(cardNumber) {
    const cardValidator = /^(?:3[47][0-9]{13})$/;

    if (cardNumber.match(cardValidator)) {
        return true;
    } else {
        return false;
    }
}

// Remove error border of selected element
function removeErrorBorder(elementID) {
    document.getElementById(elementID).style.border = '1px solid transparent';
    document.getElementById(elementID).style.borderBottom = '1px solid #ccc';
    document.getElementById(elementID).style.borderRadius = '0';
}

// Add error broder to selected element
function addErrorBorder(elementID) {
    document.getElementById(elementID).style.border = '1px solid #f44336';
    document.getElementById(elementID).style.borderRadius = '5px';
}

// Clear color of all credit card logos
function clearLogoColor() {
    document.getElementById('visalogo').classList.remove('activelogo');
    document.getElementById('mastercardlogo').classList.remove('activelogo');
    document.getElementById('discoverlogo').classList.remove('activelogo');
    document.getElementById('amexlogo').classList.remove('activelogo');
}