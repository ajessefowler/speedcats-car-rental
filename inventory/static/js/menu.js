document.addEventListener('DOMContentLoaded', function(event) {
    let menuOut = false;
		
		document.getElementById('menushade').addEventListener('click', function() {
			closeMenu();
		})

    document.getElementById('menubutton').addEventListener('click', function() {
			if (!menuOut) {
				menuOut = true;
				document.getElementById('menushade').style.display = 'block';
				document.querySelector('nav').style.animation = 'menuOut .3s ease forwards';
				document.getElementById('menushade').style.animation = 'fadeIn .3s ease forwards';
				document.getElementById('menubutton').innerHTML = 'chevron_left';
			} else {
				closeMenu();
			}
    });
		
		function closeMenu() {
			menuOut = false;
			document.querySelector('nav').style.animation = 'menuIn .3s ease forwards';
			document.getElementById('menushade').style.animation = 'fadeOut .3s ease forwards';
			document.getElementById('menubutton').innerHTML = 'menu';
			setTimeout(function() {
				document.getElementById('menushade').style.display = 'none';
			}, 300);
		}
});