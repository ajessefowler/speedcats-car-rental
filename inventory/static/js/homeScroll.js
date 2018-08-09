document.addEventListener('DOMContentLoaded', function(event) {
    // Scroll down to content when home page arrow is clicked
    document.getElementById('desktoparrow').addEventListener('click', function() {
        const content = document.getElementById('homecontent');
        zenscroll.to(content);
    });
});