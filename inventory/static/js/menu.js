document.addEventListener('DOMContentLoaded', function(event) {
    let menuOut = false;
		
	// Close menu when shade is clicked
	document.getElementById('menushade').addEventListener('click', function() {
		closeMenu();
	});

	// Open or close menu when menu text is clicked
	document.getElementById('menubuttontext').addEventListener('click', function() {
		if (!menuOut) {
			openMenu();
		} else {
			closeMenu();
		}
	});

	// Open or close menu when menu button is clicked
    document.getElementById('menubutton').addEventListener('click', function() {
		if (!menuOut) {
			openMenu();
		} else {
			closeMenu();
		}
	});
		
	// Animate the menu opening
	function openMenu() {
		menuOut = true;
		document.getElementById('menumiddle').style.animation = 'fadeOut .2s ease forwards';
		document.getElementById('menubottom').style.animation = 'bottomToArrow .3s ease forwards';
		document.getElementById('menutop').style.animation = 'topToArrow .3s ease forwards';
		document.getElementById('menushade').style.display = 'block';
		document.querySelector('nav').style.animation = 'menuOut .3s ease forwards';
		document.getElementById('menushade').style.animation = 'fadeIn .3s ease forwards';
	}
		
	// Animate the menu closing
	function closeMenu() {
		menuOut = false;
		document.getElementById('menumiddle').style.animation = 'fadeIn .6s ease forwards';
		document.getElementById('menubottom').style.animation = 'bottomToButton .3s ease forwards';
		document.getElementById('menutop').style.animation = 'topToButton .3s ease forwards';
		document.querySelector('nav').style.animation = 'menuIn .3s ease forwards';
		document.getElementById('menushade').style.animation = 'fadeOut .3s ease forwards';
		setTimeout(function() {
			document.getElementById('menushade').style.display = 'none';
		}, 300);
	}
});