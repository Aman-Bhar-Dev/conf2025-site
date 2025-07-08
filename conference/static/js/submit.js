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

// Show/hide custom institute input
document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("institute-select");
  const customWrapper = document.getElementById("custom-institute-wrapper");

  select.addEventListener("change", function () {
    customWrapper.classList.toggle("hidden", this.value !== "Other");
  });

  // Hamburger toggle
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("nav-links");

  hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("show");
  });
});
setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.display = 'none';
    });
}, 5000); // hide after 5 seconds