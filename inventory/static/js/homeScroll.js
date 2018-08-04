document.addEventListener('DOMContentLoaded', function(event) {
    document.getElementById('desktoparrow').addEventListener('click', function() {
        const content = document.getElementById('homecontent');
        zenscroll.to(content);
    });
});