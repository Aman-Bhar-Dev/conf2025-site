// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
  const bgDiv = document.querySelector('.about-page-bg');

  // Array of image paths
  const images = [
    '/static/images/bhutan1.jpg',
    '/static/images/bhutan2.jpg',
    '/static/images/bhutan3.jpg',
    '/static/images/bhutan4.jpg',
    '/static/images/bhutan5.jpg'
  ];

  let currentIndex = 0;

  // Preload images for smoother transitions
  images.forEach(src => {
    const img = new Image();
    img.src = src;
  });

  // Function to change background image with a fade effect
  function changeBackground() {
    currentIndex = (currentIndex + 1) % images.length;
    bgDiv.style.opacity = '0.02';  // briefly fade out

    setTimeout(() => {
      bgDiv.style.backgroundImage = `url('${images[currentIndex]}')`;
      bgDiv.style.opacity = '0.05';  // fade back in
    }, 500); // match transition duration
  }

  // Change image every 10 seconds
  setInterval(changeBackground, 10000);
});
  document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.getElementById("nav-links");

    menuToggle.addEventListener("click", function () {
      navLinks.classList.toggle("active");
    });
  });
