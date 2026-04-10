document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  if (!signupForm) return;

  const fullNameInput = document.getElementById("full_name");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const confirmInput = document.getElementById("confirm-password");
  const roleSelect = document.getElementById("role");
  const submitBtn = document.getElementById("submit-btn");
  const strengthIndicator = document.getElementById("password-strength");
  const matchIndicator = document.getElementById("password-match");
  const togglePass = document.getElementById("toggle-password");
  const toggleConfirm = document.getElementById("toggle-confirm");
  const welcomeMessage = document.getElementById("welcome-message");

  let errorBox = document.getElementById("error-box");
  if (!errorBox) {
    errorBox = document.createElement("div");
    errorBox.id = "error-box";
    errorBox.className = "error-box";
    signupForm.prepend(errorBox);
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  passwordInput.addEventListener("input", () => {
    const pwd = passwordInput.value.trim();
    const level = getPasswordStrength(pwd);

    strengthIndicator.className = "password-strength";
    if (!pwd) {
      strengthIndicator.textContent = "";
      checkMatch();
      return;
    }

    strengthIndicator.textContent =
      level === "weak" ? "Weak 🔴" :
      level === "medium" ? "Medium 🟡" :
      "Strong 🟢";

    strengthIndicator.classList.add(level);
    checkMatch();
  });

  confirmInput.addEventListener("input", checkMatch);

  function checkMatch() {
    const password = passwordInput.value;
    const confirm = confirmInput.value;
    const strength = getPasswordStrength(password);

    if (!confirm) {
      matchIndicator.textContent = "";
      submitBtn.disabled = true;
      return;
    }

    if (password === confirm && strength !== "weak") {
      matchIndicator.textContent = "Passwords match ✅";
      matchIndicator.className = "password-match success";
      submitBtn.disabled = false;
    } else if (password !== confirm) {
      matchIndicator.textContent = "Passwords do not match ❌";
      matchIndicator.className = "password-match error";
      submitBtn.disabled = true;
    } else {
      matchIndicator.textContent = "Password is too weak ❌";
      matchIndicator.className = "password-match error";
      submitBtn.disabled = true;
    }
  }

  function toggleVisibility(input, toggle) {
    if (!input || !toggle) return;
    const isHidden = input.type === "password";
    input.type = isHidden ? "text" : "password";
    toggle.textContent = isHidden ? "🙈" : "👁";
  }

  if (togglePass) {
    togglePass.addEventListener("click", () => toggleVisibility(passwordInput, togglePass));
  }

  if (toggleConfirm) {
    toggleConfirm.addEventListener("click", () => toggleVisibility(confirmInput, toggleConfirm));
  }

  function getPasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    if (score <= 1) return "weak";
    if (score <= 3) return "medium";
    return "strong";
  }

  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";

    const full_name = fullNameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const confirm = confirmInput.value.trim();
    const role = roleSelect.value;

    if (!full_name || !email || !password || !confirm || !role) {
      return showError("Please fill all fields.");
    }

    if (password !== confirm) {
      return showError("Passwords do not match.");
    }

    try {
      const signupRes = await fetch("/signup/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ full_name, email, password, role }),
        credentials: "include",
      });

      const signupData = await signupRes.json();
      if (!signupRes.ok) {
        return showError(signupData.error || "Signup failed.");
      }

      const loginRes = await fetch("/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ email, password }),
        credentials: "include",
      });

      if (!loginRes.ok) {
        return showError("Registered, but auto-login failed. Login manually.");
      }

      if (welcomeMessage) {
        welcomeMessage.innerHTML = `
          🎉 Welcome to Skillvine, <strong>${full_name}</strong>!<br>
          Role: <strong>${role}</strong><br>
          Redirecting...
        `;
      }

      setTimeout(() => {
        window.location.href = signupData.redirect || "/dashboard/";
      }, 1800);

    } catch (err) {
      console.error(err);
      showError("Network or server error. Try again.");
    }
  });

  function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.add("show");
    setTimeout(() => errorBox.classList.remove("show"), 4000);
  }
});