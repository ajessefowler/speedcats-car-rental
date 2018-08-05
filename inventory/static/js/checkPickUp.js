document.addEventListener('DOMContentLoaded', function(event) {
    document.getElementById('startbutton').addEventListener('click', function() {
        const start = document.getElementById('startbutton');
        const newValue = document.getElementById('pickuplocationid').value;

        document.getElementById('confirmshade').addEventListener('click', function() {
            document.getElementById('confirmshade').style.animation = 'fadeOut .4s ease forwards';
            document.getElementById('changevehiclecard').style.animation = 'timeDown .4s ease forwards';
            setTimeout(function() {
                document.getElementById('confirmshade').style.display = 'none';
            }, 400);
        });

        document.getElementById('closevehiclecard').addEventListener('click', function() {
            document.getElementById('confirmshade').style.animation = 'fadeOut .4s ease forwards';
            document.getElementById('changevehiclecard').style.animation = 'timeDown .4s ease forwards';
            setTimeout(function() {
                document.getElementById('confirmshade').style.display = 'none';
            }, 400);
        });

        if (newValue !== storeID) {
            start.onclick = null;
            document.getElementById('confirmshade').style.display = 'block';
            document.getElementById('confirmshade').style.animation = 'fadeIn .4s ease forwards';
            document.getElementById('changevehiclecard').style.animation = 'timeUp .4s ease forwards';
            document.getElementById('pickuplocationcontinue').addEventListener('click', function() {
                document.getElementById('selectlocation').submit();
            });
        }
    });
});