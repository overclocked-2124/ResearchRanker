document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('nav');
    const navbarPosition = navbar.offsetTop;

    function handleScroll() {
        if (window.pageYOffset > navbarPosition) {
            navbar.classList.add('nav-fixed');
        } else {
            navbar.classList.remove('nav-fixed');
        }
    }

    window.addEventListener('scroll', handleScroll);
});