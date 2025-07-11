function checkPasswordStrength(password) {
  const strengthText = document.getElementById("passwordStrength");
  let strength = 0;

  if (password.length >= 8) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[\W]/.test(password)) strength++;

  if (strength === 0) {
    strengthText.textContent = '';
    strengthText.className = 'strength-indicator';
  } else if (strength < 3) {
    strengthText.textContent = 'Weak password';
    strengthText.className = 'strength-indicator strength-weak';
  } else if (strength === 3) {
    strengthText.textContent = 'Moderate password';
    strengthText.className = 'strength-indicator strength-medium';
  } else {
    strengthText.textContent = 'Strong password';
    strengthText.className = 'strength-indicator strength-strong';
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("password").addEventListener("input", function () {
    checkPasswordStrength(this.value);
  });

  document.querySelector("form").addEventListener("submit", function (e) {
    if (!validateForm()) {
      e.preventDefault();
    }
  });
});
           
