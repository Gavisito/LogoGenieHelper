        function dropdownmenu() {
            var links = document.querySelector('.links');

            if (links.style.display === 'none' || links.style.display === '') {
                links.style.display = 'flex';
            } else {
                links.style.display = 'none';
            }
        }
        window.addEventListener('scroll', function () {
            var navbar = document.getElementById('navbar');
            if (window.scrollY > 0) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });