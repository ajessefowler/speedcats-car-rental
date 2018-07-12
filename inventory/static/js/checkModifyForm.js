// Turn done button orange and activate click listener
function checkFormCompletion() {
    const modify = document.getElementById('modifybutton');
    modify.style.backgroundColor = '#FF5722';
    modify.style.color = '#FFFFFF';
    modify.addEventListener('click', function() {
        document.getElementById('modifylocation').submit();
    });
}