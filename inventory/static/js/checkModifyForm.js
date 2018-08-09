// Verifies modification and displays confirmation
document.addEventListener('DOMContentLoaded', function(event) {
    const modify = document.getElementById('modifybutton');
    const vehiclePrice = parseFloat(document.getElementById('vehicleprice').value);
    const initialTotal =  parseFloat(document.getElementById('initialtotal').value);

    // Set up event listeners to close confimation
    document.getElementById('confirmshade').addEventListener('click', function() {
        closeConfirm();
    });

    document.getElementById('closeconfirmation').addEventListener('click', function() {
        closeConfirm();
    });

    // Submit form on confirm button click
    document.getElementById('confirmcancelbutton').addEventListener('click', function() {
        document.getElementById('modifylocation').submit();
    });

    modify.style.backgroundColor = '#FF5722';
    modify.style.color = '#FFFFFF';

    // Perform calculations and animations when done button is clicked
    modify.addEventListener('click', function() {
        
        const pickupStr = document.getElementById('pickuptimeformat').value;
        const pickup = formatDate(pickupStr);
        const dropoffStr = document.getElementById('dropofftimeformat').value;
        const dropoff = formatDate(dropoffStr);

        // Find the number of days
        const diff = Math.abs(dropoff.getTime() - pickup.getTime());
        const diffDays = Math.ceil(diff / (1000 * 3600 * 24) + 1);

        // Calculate pricing
        const subtotal = parseFloat(vehiclePrice * diffDays).toFixed(2);
        const tax = parseFloat(subtotal * 0.07).toFixed(2);
        const total = (parseFloat(subtotal) + parseFloat(tax)).toFixed(2);

        // Get difference from new price to old price
        const priceDiff = Math.abs(total - initialTotal).toFixed(2);

        // Update page with new pricing
        document.getElementById('subtotal').value = subtotal;
        document.getElementById('tax').value = tax;
        document.getElementById('total').value = total;
        document.getElementById('displaysubtotal').innerHTML = 'Subtotal: $' + subtotal;
        document.getElementById('displaytax').innerHTML = 'Tax: $' + tax;
        document.getElementById('displaytotal').innerHTML = 'Total: $' + total;

        // Update confirmation to display if price is higher or lower
        if (total > initialTotal) {
            document.getElementById('priceupdate').innerHTML = 'Your price will increase by $' + priceDiff + '.';
        } else if (total < initialTotal) {
            document.getElementById('priceupdate').innerHTML = 'Your price will decrease by $' + priceDiff + '.';
        }

        // Animate confirmation card
        document.getElementById('confirmshade').style.display = 'block';
        document.getElementById('confirmshade').style.animation = 'fadeIn .4s ease forwards';
        document.getElementById('confirmcard').style.animation = 'confirmUp .4s ease forwards';
    });

    // Slide the confirmation card back down
    function closeConfirm() {
        document.getElementById('confirmshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById('confirmcard').style.animation = 'confirmDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('confirmshade').style.display = 'none';
        }, 400);
    }

    // Format date as a Date object for easier use
    function formatDate(dateStr) {
        const year = dateStr.substring(0,4);
        const month = parseInt(dateStr.substring(5,7) - 1);
        const day = dateStr.substring(8,10);
        const date = new Date(year, month, day);
        return date;
    }
});