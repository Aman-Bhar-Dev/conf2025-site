document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');

    // Toggle icon between ☰ and ✖
    if (navLinks.classList.contains('show')) {
      menuToggle.innerHTML = '&times;'; // ✖
    } else {
      menuToggle.innerHTML = '&#9776;'; // ☰
    }
  });
});
