document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  // Theme toggle
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    themeToggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
  });

  // Mobile menu toggle
  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });

  // Deadline setup
  const targetDate = new Date("July 30, 2025 00:00:00").getTime();
  const now = new Date().getTime();

  // Utility to hide buttons
  const hideButton = (selector) => {
    const btn = document.querySelector(selector);
    if (btn) btn.style.display = "none";
  };

  if (now >= targetDate) {
    // Hide countdown and label
    const countdownEl = document.getElementById("countdown");
    const countdownLabel = document.querySelector(".countdown-label");

    if (countdownEl) countdownEl.innerHTML = "<p class='closed'>Submission Closed</p>";
    if (countdownLabel) countdownLabel.style.display = "none";

    // Hide buttons
    hideButton("a[href$='submit']");
    hideButton("a[href$='signup']");
    hideButton("a[href$='visitor_registration']");
  } else {
    // Live countdown
    const countdown = () => {
      const gap = targetDate - new Date().getTime();
      const day = 1000 * 60 * 60 * 24;
      const hour = 1000 * 60 * 60;
      const minute = 1000 * 60;

      document.getElementById("days").innerText = String(Math.floor(gap / day)).padStart(2, '0');
      document.getElementById("hours").innerText = String(Math.floor((gap % day) / hour)).padStart(2, '0');
      document.getElementById("minutes").innerText = String(Math.floor((gap % hour) / minute)).padStart(2, '0');
    };

    setInterval(countdown, 1000);
  }
});
