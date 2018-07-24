document.addEventListener('DOMContentLoaded', function(event) {

    document.getElementById('popupshade').addEventListener('click', function() {
        closeCard();
    })

    if (!document.getElementById('deletebutton').classList.contains('disabledbutton')) {
        document.getElementById('deletebutton').addEventListener('click', function() {
            document.getElementById('cancelconfirmation').style.animation = 'cardUp .4s ease forwards';
            document.getElementById('popupshade').style.display = 'block';
            document.getElementById('popupshade').style.animation = 'fadeIn .4s ease forwards';
        });

        document.getElementById('closeconfirmation').addEventListener('click', function() {
            closeCard();
        })
    }

    function closeCard() {
        document.getElementById('cancelconfirmation').style.animation = 'cardDown .4s ease forwards';
        document.getElementById('popupshade').style.animation = 'fadeOut .4s ease forwards';
        setTimeout(function() {
            document.getElementById('popupshade').style.display = 'none';
        }, 400);
    }
});