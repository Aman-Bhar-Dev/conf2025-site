document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  // Toggle theme
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    themeToggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
  });

  // Mobile menu toggle
  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });

  // Countdown timer
  const targetDate = new Date("August 06, 2025 00:00:00").getTime();
  const countdown = () => {
    const now = new Date().getTime();
    const gap = targetDate - now;

    const day = 1000 * 60 * 60 * 24;
    const hour = 1000 * 60 * 60;
    const minute = 1000 * 60;
    document.getElementById("days").innerText = String(Math.floor(gap / day)).padStart(2, '0');
    document.getElementById("hours").innerText = String(Math.floor((gap % day) / hour)).padStart(2, '0');
    document.getElementById("minutes").innerText = String(Math.floor((gap % hour) / minute)).padStart(2, '0');
    
  };

  setInterval(countdown, 1000);
});
