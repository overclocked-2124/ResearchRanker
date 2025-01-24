window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

window.addEventListener('DOMContentLoaded', function () {
    const signupCard = document.querySelector('#signupcard');
    const signinCard = document.querySelector('#signincard');
    signupCard.style.display = 'none';
    signinCard.style.display = 'block';
  });

  function signup(event) {
    event.preventDefault();
    const signupCard = document.querySelector('#signupcard');
    const signinCard = document.querySelector('#signincard');
    signupCard.style.display = 'block';
    signinCard.style.display = 'none';
  }

  function signin(event) {
    event.preventDefault();
    const signupCard = document.querySelector('#signupcard');
    const signinCard = document.querySelector('#signincard');
    signupCard.style.display = 'none';
    signinCard.style.display = 'block';
  }