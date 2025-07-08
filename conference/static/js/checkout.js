let visitorCount = 0;

function addVisitor() {
  const section = document.getElementById('visitor-section');
  const div = document.createElement('div');
  div.className = 'visitor-block';
  div.setAttribute('data-index', visitorCount);

  div.innerHTML = `
    <button type="button" class="remove-button" onclick="removeVisitor(this)">×</button>

    <label>Visitor Name</label>
    <input type="text" name="visitor_name_${visitorCount}" required>

    <label>Email</label>
    <input type="email" name="visitor_email_${visitorCount}" required>

    <label>Mode of Attendance</label>
    <select name="visitor_mode_${visitorCount}" required onchange="updateTotal()">
      <option value="Offline">Offline</option>
      <option value="Online">Online</option>
    </select>

    <label>Upload Identity Proof</label>
    <input type="file" name="visitor_proof_${visitorCount}" accept=".pdf,.png,.jpg,.jpeg">
    <hr>
  `;

  section.appendChild(div);
  visitorCount++;
  document.getElementById('visitor-count').value = visitorCount;
  updateTotal();
}

function removeVisitor(button) {
  const block = button.closest('.visitor-block');
  if (block) {
    block.remove();
    updateTotal();
  }
}

function isDiscountEligible(affiliation) {
  return affiliation.toLowerCase().includes("assam university");
}

function updateTotal() {
  let total = 0;

  const authorMode = document.querySelector('select[name="author_mode"]')?.value;
  const mainInstitute = document.querySelector('input[name="institute_name"]')?.value?.toLowerCase() || '';
  const category = document.getElementById("category-value")?.value?.toLowerCase() || '';

  // Author fee
  if (authorMode === 'Offline') {
    if (category === 'corporate') {
      total += isDiscountEligible(mainInstitute) ? 19000 : 20000;
    } else {
      total += isDiscountEligible(mainInstitute) ? 15000 : 16000;
    }
  } else if (authorMode === 'Online') {
    total += category === 'corporate' ? 2000 : 1000;
  }

  // Co-authors
  const coauthorSelects = document.querySelectorAll('[name^="coauthor_mode_"]');
  coauthorSelects.forEach((select, index) => {
    const affiliationField = document.querySelector(`[name="coauthor_affiliation_${index}"]`);
    const affiliation = affiliationField?.value?.toLowerCase() || '';

    if (select.value === 'Offline') {
      if (category === 'corporate') {
        total += isDiscountEligible(affiliation) ? 19000 : 20000;
      } else {
        total += isDiscountEligible(affiliation) ? 15000 : 16000;
      }
    } else if (select.value === 'Online') {
      total += category === 'corporate' ? 2000 : 1000;
    }
  });

  // Visitors
  for (let i = 0; i < visitorCount; i++) {
    const mode = document.querySelector(`select[name="visitor_mode_${i}"]`);
    if (mode) {
      if (mode.value === 'Offline') total += 16000;
      else if (mode.value === 'Online') total += 1000;
    }
  }

  document.getElementById('total-amount').innerText = total;
}
