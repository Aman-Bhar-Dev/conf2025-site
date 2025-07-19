let coAuthorCount = 0;

function addCoAuthor() {
  const container = document.getElementById("coauthor-container");
  const entry = document.createElement("div");
  entry.classList.add("co-author-entry");

  entry.innerHTML = `
    <div class="co-author-group">
      <label>First Name</label>
      <input type="text" name="coAuthorFirstName${coAuthorCount}" required>
      <label>Last Name</label>
      <input type="text" name="coAuthorLastName${coAuthorCount}" required>
      <label>Email</label>
      <input type="email" name="coAuthorEmail${coAuthorCount}" required>
      <label>Affiliation</label>
      <input type="text" name="coAuthorAffiliation${coAuthorCount}" required>
      <button type="button" class="remove-button" onclick="removeCoAuthor(this)">×</button>
    </div>
  `;

  container.appendChild(entry);
  coAuthorCount++;
}

function removeCoAuthor(button) {
  const group = button.closest(".co-author-entry");
  group.remove();
}

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

