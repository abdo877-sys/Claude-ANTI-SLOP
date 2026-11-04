// Request-access form: validation, loading, success and error states.
// Set FORM_ENDPOINT to a real endpoint (Formspree, your API, etc.) to send requests.
// While it is empty, the form says plainly that it is not connected — it never pretends to succeed.
const FORM_ENDPOINT = "";

const form = document.getElementById("access-form");
const status = document.getElementById("form-status");
const button = form.querySelector('button[type="submit"]');

const rules = {
  name: (v) => (v.trim() ? "" : "Please enter your name."),
  shop: (v) => (v.trim() ? "" : "Please enter your shop's name and neighbourhood."),
  phone: (v) => (/^\+?[\d\s]{8,15}$/.test(v.trim()) ? "" : "Enter a phone number with 8 to 15 digits, e.g. +253 77 12 34 56."),
};

function showError(field, message) {
  const input = form.elements[field];
  const error = document.getElementById(`${field}-error`);
  input.setAttribute("aria-invalid", message ? "true" : "false");
  error.textContent = message;
  error.hidden = !message;
}

// Errors appear on blur, but clear while typing — never on blur — so the layout
// doesn't shift under the pointer when the user moves to the submit button.
for (const field of Object.keys(rules)) {
  const input = form.elements[field];
  input.addEventListener("blur", () => {
    const message = input.value ? rules[field](input.value) : "";
    if (message) showError(field, message);
  });
  input.addEventListener("input", () => {
    if (input.getAttribute("aria-invalid") === "true" && !rules[field](input.value)) showError(field, "");
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "";
  delete status.dataset.kind;

  let firstInvalid = null;
  for (const [field, check] of Object.entries(rules)) {
    const message = check(form.elements[field].value);
    showError(field, message);
    if (message && !firstInvalid) firstInvalid = form.elements[field];
  }
  if (firstInvalid) {
    firstInvalid.focus();
    return;
  }

  if (!FORM_ENDPOINT) {
    status.dataset.kind = "error";
    status.textContent = "This form isn’t connected to a server yet, so nothing was sent. (Site owner: set FORM_ENDPOINT in contact.js.)";
    return;
  }

  button.disabled = true;
  button.setAttribute("aria-busy", "true");
  button.textContent = "Sending…";
  try {
    const response = await fetch(FORM_ENDPOINT, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(String(response.status));
    form.reset();
    status.textContent = "Thanks — your request was sent. We’ll contact you within a few days.";
  } catch {
    status.dataset.kind = "error";
    status.textContent = "Your request couldn’t be sent. Check your connection and try again — your answers are still here.";
  } finally {
    button.disabled = false;
    button.removeAttribute("aria-busy");
    button.textContent = "Send request";
  }
});
