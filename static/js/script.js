document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const mobileMenu = document.getElementById("mobile-menu");
    const content = document.getElementById("content");
  
    menuToggle.addEventListener("click", function () {
      if (mobileMenu.classList.contains("hidden")) {
        mobileMenu.classList.remove("hidden");
        mobileMenu.classList.add("flex", "flex-col", "space-y-4");
        content.classList.add("mt-40"); // Push content down
      } else {
        mobileMenu.classList.add("hidden");
        mobileMenu.classList.remove("flex", "flex-col", "space-y-4");
        content.classList.remove("mt-40"); // Reset content position
      }
    });
  });

  
  document.addEventListener("DOMContentLoaded", function () {
    const copyBtn = document.getElementById("copy-btn");
    const accountNumber = document.getElementById("account-number").innerText;

    copyBtn.addEventListener("click", function () {
        navigator.clipboard.writeText(accountNumber)
            .then(() => alert("Account Number Copied!"))
            .catch(err => console.error("Error copying text: ", err));
    });
});


// register
document.addEventListener("DOMContentLoaded", function () {
  function setupPasswordToggle(toggleSelector) {
      const toggles = document.querySelectorAll(toggleSelector);
      
      toggles.forEach(toggle => {
          const input = document.querySelector(toggle.dataset.target);
          
          if (toggle && input) {
              toggle.addEventListener("click", function () {
                  if (input.type === "password") {
                      input.type = "text";
                      toggle.classList.replace("ri-eye-off-line", "ri-eye-line");
                  } else {
                      input.type = "password";
                      toggle.classList.replace("ri-eye-line", "ri-eye-off-line");
                  }
              });
          }
      });
  }

  // Initialize password toggles
  setupPasswordToggle(".toggle-password");
});



// index 


