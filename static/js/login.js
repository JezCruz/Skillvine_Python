document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;

  const emailInput = document.getElementById("login-email");
  const passwordInput = document.getElementById("login-password");
  const submitBtn = loginForm.querySelector('button[type="submit"]');
  const errorBox = document.getElementById("error-box");
  const togglePass = document.getElementById("toggle-login-password");

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

  if (togglePass) {
    togglePass.addEventListener("click", (e) => {
      e.preventDefault();
      const isHidden = passwordInput.type === "password";
      passwordInput.type = isHidden ? "text" : "password";
      togglePass.textContent = isHidden ? "🙈" : "👁";
    });
  }

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      return showError("Please enter both email and password.");
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Logging in...";

    try {
      const response = await fetch("/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ email, password }),
        credentials: "include",
      });

      const contentType = response.headers.get("Content-Type") || "";
      let data = {};

      if (contentType.includes("application/json")) {
        data = await response.json();
      }

      if (!response.ok) {
        return showError(data.error || "Invalid email or password.");
      }

      showNotice("Welcome back!", "success", 800);

      setTimeout(() => {
        document.body.classList.add("fade-out");

        setTimeout(() => {
          window.location.href = data.redirect || "/dashboard/";
        }, 350);
      }, 500);

    } catch (err) {
      console.error(err);
      showError("Network or server error. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Login";
    }
  });

  function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.add("show");
    setTimeout(() => errorBox.classList.remove("show"), 4000);
  }

  function showNotice(message, type = "info", duration = 3000) {
    let el = document.getElementById("top-notice");
    if (!el) {
      el = document.createElement("div");
      el.id = "top-notice";
      el.className = "top-notice";
      document.body.appendChild(el);
    }

    el.textContent = message;
    el.classList.add("show");
    el.classList.remove("hide");

    if (duration > 0) {
      setTimeout(() => {
        el.classList.remove("show");
        el.classList.add("hide");
      }, duration);
    }
  }
});