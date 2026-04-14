document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("teacherProfileModal");
  const modalBody = document.getElementById("teacherProfileModalBody");
  const closeBtn = document.getElementById("closeTeacherProfileModal");
  const openButtons = document.querySelectorAll(".open-profile-modal");

  openButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const url = btn.dataset.url;
      modal.classList.add("show");
      modalBody.innerHTML = "<p>Loading...</p>";

      try {
        const response = await fetch(url, {
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const html = await response.text();
        modalBody.innerHTML = html;
      } catch (error) {
        modalBody.innerHTML = "<p>Failed to load teacher profile.</p>";
      }
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.remove("show");
    });
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("show");
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      modal.classList.remove("show");
    }
  });
});