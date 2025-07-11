document.addEventListener('DOMContentLoaded', () => {
  const bgDiv = document.querySelector('.about-page-bg');

  // Background image carousel
  const images = [
    '/static/images/bhutan1.jpg',
    '/static/images/bhutan2.jpg',
    '/static/images/bhutan3.jpg',
    '/static/images/bhutan4.jpg',
    '/static/images/bhutan5.jpg'
  ];
  let currentIndex = 0;

  images.forEach(src => {
    const img = new Image();
    img.src = src;
  });

  function changeBackground() {
    currentIndex = (currentIndex + 1) % images.length;
    bgDiv.style.opacity = '0.02';

    setTimeout(() => {
      bgDiv.style.backgroundImage = `url('${images[currentIndex]}')`;
      bgDiv.style.opacity = '0.05';
    }, 500);
  }

  setInterval(changeBackground, 10000);

  // Hamburger menu toggle
  const menuToggle = document.getElementById("menu-toggle");
  const navLinks = document.getElementById("nav-links");

  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });
});
