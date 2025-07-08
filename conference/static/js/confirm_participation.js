document.getElementById("participation-form").addEventListener("submit", function (e) {
  const authorMode = document.getElementById("author_mode").value;
  const authorProof = document.querySelector("input[name='author_identity_proof']").files.length;

  if (!authorMode || authorProof === 0) {
    alert("Please select main author mode and upload identity proof.");
    e.preventDefault();
    return;
  }

  const coauthorSelects = document.querySelectorAll("select[name^='coauthor_mode_']");
  const coauthorProofs = document.querySelectorAll("input[name^='coauthor_proof_']");

  coauthorSelects.forEach((select, index) => {
    const mode = select.value;
    const proof = coauthorProofs[index].files.length;

    if ((mode === "Offline" || mode === "Online") && proof === 0) {
      alert("Please upload identity proof for attending co-authors.");
      e.preventDefault();
    }
  });
});
