document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
    menuToggle.innerHTML = navLinks.classList.contains('show') ? '&times;' : '&#9776;';
  });

  // Optional: auto-close menu on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('show');
      menuToggle.innerHTML = '&#9776;';
    });
  });
});
