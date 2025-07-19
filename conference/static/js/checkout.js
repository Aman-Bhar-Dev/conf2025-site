document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("checkout-form");
  const visitorsContainer = document.getElementById("visitors-container");
  const addVisitorBtn = document.getElementById("add-visitor");
  const summaryContainer = document.getElementById("payment-summary");
  let visitorCount = 0;

function getFee(category, mode, institute) {
  if (!mode) return 0;

  // Visitor flat fee
  if (category === "NonPresenter") return 15000;

  // International
  if (category === "International") return mode === "Offline" ? 20750 : 8300;

  // Corporate
  if (category === "Corporate") return mode === "Offline" ? 20000 : 2000;

  // Academician / Student
  if (["Academician", "Student"].includes(category)) {
    const inst = (institute || "").toLowerCase().trim();
    if (mode === "Offline") {
      return inst.includes("assam university") ? 15000 : 16000;
    } else if (mode === "Online") {
      return 1000;
    }
  }

  return 0;
}


  function toggleProofVisibility() {
    // Main Author
    const authorSelect = form.querySelector("select[name='author_mode']");
    const authorProofWrapper = form.querySelector("input[name='author_identity_proof']")?.closest(".proof-wrapper");
    if (authorProofWrapper && authorSelect) {
      authorProofWrapper.style.display = authorSelect.value === "Offline" ? "block" : "none";
    }

    // Co-authors
    document.querySelectorAll("[id^='coauthor-block-']").forEach((block, i) => {
      const select = block.querySelector(`select[name='coauthor_mode_${i}']`);
      const proofInput = block.querySelector(`input[name='coauthor_proof_${i}']`);
      const proofWrapper = proofInput?.closest(".proof-wrapper");
      if (proofWrapper && select) {
        proofWrapper.style.display = select.value === "Offline" ? "block" : "none";
      }
    });

    // Visitors
    visitorsContainer.querySelectorAll(".visitor-block").forEach(block => {
      const select = block.querySelector("select[name^='visitor_mode_']");
      const proofWrapper = block.querySelector(".proof-wrapper");
      if (proofWrapper && select) {
        proofWrapper.style.display = select.value === "Offline" ? "block" : "none";
      }
    });
  }

  function calculateTotalFee() {
    let total = 0;
    let breakdown = [];

    // Main Author
    const authorModeField = form.querySelector("select[name='author_mode']");
    const authorMode = authorModeField?.value || "";
    const authorCategory = authorModeField?.dataset.category || "Student";
    const authorInstitute = authorModeField?.dataset.institute || "";
    const authorFee = getFee(authorCategory, authorMode, authorInstitute);
    total += authorFee;
    if (authorMode) {
      breakdown.push(`Main Author: ₹${authorFee.toLocaleString("en-IN")}`);
    }

    // Co-authors
    document.querySelectorAll("[id^='coauthor-block-']").forEach((block, i) => {
      const modeField = block.querySelector(`select[name='coauthor_mode_${i}']`);
      const mode = modeField?.value || "";
      const category = modeField?.getAttribute("data-category") || "Student";
      const institute = modeField?.getAttribute("data-institute") || "";
      const fee = getFee(category, mode, institute);
      total += fee;
      if (mode) {
        breakdown.push(`Co-author ${i + 1}: ₹${fee.toLocaleString("en-IN")}`);
      }
    });

    // Visitors
    const visitors = visitorsContainer.querySelectorAll(".visitor-block");
    visitors.forEach((block, i) => {
      const fee = 15000;
      total += fee;
      breakdown.push(`Visitor ${i + 1}: ₹${fee.toLocaleString("en-IN")}`);
    });

    // Update totals
    document.getElementById("total-amount").innerText = total.toLocaleString("en-IN");

    if (summaryContainer) {
      summaryContainer.innerHTML = "<h3>Payment Summary</h3><ul>" +
        breakdown.map(line => `<li>${line}</li>`).join("") +
        `</ul><p><strong>Total Payable:</strong> ₹${total.toLocaleString("en-IN")}</p>`;
    }
  }

  form.addEventListener("change", () => {
    toggleProofVisibility();
    calculateTotalFee();
  });

  addVisitorBtn.addEventListener("click", () => {
    const visitorDiv = document.createElement("div");
    visitorDiv.className = "visitor-block";
    visitorDiv.innerHTML = `
      <hr>
      <label>Visitor Name:</label>
      <input type="text" name="visitor_name_${visitorCount}" required>

      <label>Email:</label>
      <input type="email" name="visitor_email_${visitorCount}" required>

      <label>Phone:</label>
      <input type="text" name="visitor_phone_${visitorCount}" required>

      <label>Address:</label>
      <textarea name="visitor_address_${visitorCount}" required></textarea>

      <label>Gender:</label>
      <select name="visitor_gender_${visitorCount}" required>
        <option value="">-- Select --</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>

      <label>Mode of Participation:</label>
      <select name="visitor_mode_${visitorCount}" required>
        <option value="">-- Select --</option>
        <option value="Offline">Offline</option>
        <option value="Online">Online</option>
      </select>

      <div class="proof-wrapper">
        <label>Upload Identity Proof:</label>
        <input type="file" name="visitor_proof_${visitorCount}" accept=".pdf,.jpg,.jpeg,.png">
      </div>

      <button type="button" class="remove-visitor">Remove</button>
    `;

    visitorsContainer.appendChild(visitorDiv);

    visitorDiv.querySelector(".remove-visitor").addEventListener("click", () => {
      visitorsContainer.removeChild(visitorDiv);
      calculateTotalFee();
    });

    visitorDiv.querySelector(`select[name="visitor_mode_${visitorCount}"]`).addEventListener("change", () => {
      toggleProofVisibility();
      calculateTotalFee();
    });

    visitorCount++;
    toggleProofVisibility();
    calculateTotalFee();
  });

  toggleProofVisibility();
  calculateTotalFee();
});
