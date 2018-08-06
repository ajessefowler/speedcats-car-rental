document.addEventListener('DOMContentLoaded', function(event) {
    document.getElementById('registerbutton').addEventListener('click', function(event) {
        const dateInput = document.getElementById('id_date_of_birth');
        const dateOfBirth = convertDateToUTC(new Date(dateInput.value));
        const now = new Date();
        now.setFullYear(now.getFullYear() - 18);
       
        // If user is at least 18 y/o, submit form, otherwise display error
        if (dateOfBirth > now) {
            event.preventDefault();
            dateInput.style.border = '1px solid red';
        } else {
            dateInput.style.border = '1px solid transparent';
            dateInput.style.borderBottom = '1px solid #bbb';
        }
    });

    function convertDateToUTC(date) { 
        return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds()); 
    }
});