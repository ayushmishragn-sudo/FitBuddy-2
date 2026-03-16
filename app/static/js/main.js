// FitBuddy – main.js

document.addEventListener("DOMContentLoaded", () => {
  setupFormLoading();
  setupFeedbackLoading();
  setupInputValidation();
});

// ── Loading overlay for plan generation ──
function setupFormLoading() {
  const form = document.getElementById("planForm");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    // Basic client-side validation
    const name = document.getElementById("name")?.value.trim();
    const age = parseInt(document.getElementById("age")?.value);
    const weight = parseFloat(document.getElementById("weight")?.value);
    const goal = form.querySelector('input[name="goal"]:checked');
    const intensity = form.querySelector('input[name="intensity"]:checked');

    if (!name || !age || !weight || !goal || !intensity) return;

    if (age < 10 || age > 100) { e.preventDefault(); showError("Please enter a valid age (10–100)."); return; }
    if (weight < 20 || weight > 300) { e.preventDefault(); showError("Please enter a valid weight (20–300 kg)."); return; }

    showLoadingOverlay("🤖 Generating your personalized plan...", "Gemini AI is crafting your 7-day schedule");
    const btn = document.getElementById("submitBtn");
    if (btn) btn.disabled = true;
  });
}

// ── Loading overlay for feedback submission ──
function setupFeedbackLoading() {
  const form = document.getElementById("feedbackForm");
  if (!form) return;

  form.addEventListener("submit", () => {
    showLoadingOverlay("🔄 Updating your plan...", "Applying your feedback with AI");
    const btn = document.getElementById("feedbackBtn");
    if (btn) btn.disabled = true;
  });
}

// ── Show loading overlay ──
function showLoadingOverlay(text, sub) {
  const overlay = document.createElement("div");
  overlay.className = "loading-overlay";
  overlay.innerHTML = `
    <div class="loading-spinner"></div>
    <div class="loading-text">${text}</div>
    <div class="loading-sub">${sub}</div>
  `;
  document.body.appendChild(overlay);
}

// ── Show inline error ──
function showError(msg) {
  const existing = document.querySelector(".alert-error");
  if (existing) existing.remove();

  const alert = document.createElement("div");
  alert.className = "alert alert-error";
  alert.innerHTML = `<span class="alert-icon">⚠️</span> ${msg}`;

  const form = document.getElementById("planForm");
  if (form) form.parentNode.insertBefore(alert, form);

  setTimeout(() => alert.remove(), 5000);
}

// ── Input validation helpers ──
function setupInputValidation() {
  const ageInput = document.getElementById("age");
  const weightInput = document.getElementById("weight");

  if (ageInput) {
    ageInput.addEventListener("blur", () => {
      const val = parseInt(ageInput.value);
      if (ageInput.value && (val < 10 || val > 100)) {
        ageInput.style.borderColor = "var(--clr-accent)";
      } else {
        ageInput.style.borderColor = "";
      }
    });
  }

  if (weightInput) {
    weightInput.addEventListener("blur", () => {
      const val = parseFloat(weightInput.value);
      if (weightInput.value && (val < 20 || val > 300)) {
        weightInput.style.borderColor = "var(--clr-accent)";
      } else {
        weightInput.style.borderColor = "";
      }
    });
  }
}

// ── Scroll to feedback section if feedback_success ──
const feedbackCard = document.querySelector(".feedback-card");
const successAlert = document.querySelector(".alert-success");
if (successAlert && feedbackCard) {
  feedbackCard.scrollIntoView({ behavior: "smooth", block: "start" });
}
