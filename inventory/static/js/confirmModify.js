document.addEventListener('DOMContentLoaded', function(event) {
    document.getElementById('popupshade').addEventListener('click', function() {
        closeCard();
    });

    // If reservation can be deleted, add event listener to open confirmation card
    if (!document.getElementById('deletebutton').classList.contains('disabledbutton')) {
        document.getElementById('deletebutton').addEventListener('click', function() {
            document.getElementById('cancelconfirmation').style.animation = 'cardUp .4s ease forwards';
            document.getElementById('popupshade').style.display = 'block';
            document.getElementById('popupshade').style.animation = 'fadeIn .4s ease forwards';
        });

        // Close the cancel confirmation card
        document.getElementById('closeconfirmation').addEventListener('click', function() {
            closeCard();
        });
    }

    // Slide the cancel confirmation card back down
    function closeCard() {
        document.getElementById('cancelconfirmation').style.animation = 'cardDown .4s ease forwards';
        document.getElementById('popupshade').style.animation = 'fadeOut .4s ease forwards';
        setTimeout(function() {
            document.getElementById('popupshade').style.display = 'none';
        }, 400);
    }
});