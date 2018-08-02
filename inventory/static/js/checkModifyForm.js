// Turn done button orange and activate click listener
document.addEventListener('DOMContentLoaded', function(event) {
    const modify = document.getElementById('modifybutton');
    const vehiclePrice = parseFloat(document.getElementById('vehicleprice').value);
    const initialTotal =  parseFloat(document.getElementById('initialtotal').value);

    document.getElementById('confirmshade').addEventListener('click', function() {
        closeConfirm();
    });

    document.getElementById('closeconfirmation').addEventListener('click', function() {
        closeConfirm();
    });

    document.getElementById('confirmcancelbutton').addEventListener('click', function() {
        document.getElementById('modifylocation').submit();
    });

    modify.style.backgroundColor = '#FF5722';
    modify.style.color = '#FFFFFF';
    modify.addEventListener('click', function() {
        
        const pickupStr = document.getElementById('pickuptimeformat').value;
        const pickup = formatDate(pickupStr);
        const dropoffStr = document.getElementById('dropofftimeformat').value;
        const dropoff = formatDate(dropoffStr);

        const diff = Math.abs(dropoff.getTime() - pickup.getTime());
        const diffDays = Math.ceil(diff / (1000 * 3600 * 24) + 1);

        const subtotal = parseFloat(vehiclePrice * diffDays).toFixed(2);
        const tax = parseFloat(subtotal * 0.07).toFixed(2);
        const total = (parseFloat(subtotal) + parseFloat(tax)).toFixed(2);

        const priceDiff = Math.abs(total - initialTotal).toFixed(2);

        document.getElementById('subtotal').value = subtotal;
        document.getElementById('tax').value = tax;
        document.getElementById('total').value = total;

        document.getElementById('displaysubtotal').innerHTML = 'Subtotal: $' + subtotal;
        document.getElementById('displaytax').innerHTML = 'Tax: $' + tax;
        document.getElementById('displaytotal').innerHTML = 'Total: $' + total;


        if (total > initialTotal) {
            document.getElementById('priceupdate').innerHTML = 'Your price will increase by $' + priceDiff + '.';
        } else if (total < initialTotal) {
            document.getElementById('priceupdate').innerHTML = 'Your price will decrease by $' + priceDiff + '.';
        }

        // Add logic to check if vehicle is available here

        document.getElementById('confirmshade').style.display = 'block';
        document.getElementById('confirmshade').style.animation = 'fadeIn .4s ease forwards';
        document.getElementById('confirmcard').style.animation = 'confirmUp .4s ease forwards';
    });

    function closeConfirm() {
        document.getElementById('confirmshade').style.animation = 'fadeOut .4s ease forwards';
        document.getElementById('confirmcard').style.animation = 'confirmDown .4s ease forwards';
        setTimeout(function() {
            document.getElementById('confirmshade').style.display = 'none';
        }, 400);
    }

    function formatDate(dateStr) {
        const year = dateStr.substring(0,4);
        const month = parseInt(dateStr.substring(5,7) - 1);
        const day = dateStr.substring(8,10);
        const date = new Date(year, month, day);
        return date;
    }
});