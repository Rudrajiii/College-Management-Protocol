const passwordInput = document.getElementById("password");
const lowercaseIndicator = document
  .getElementById("lowercase")
  .querySelector("span");
const uppercaseIndicator = document
  .getElementById("uppercase")
  .querySelector("span");
const digitIndicator = document.getElementById("digit").querySelector("span");
const specialIndicator = document
  .getElementById("special")
  .querySelector("span");
const phoneInput = document.getElementById("phone");
const phoneInput1 = document.getElementById("phone1");
const phoneError = document.getElementById("phoneError");
const phoneError1 = document.getElementById("phoneError1");

passwordInput.addEventListener("input", function () {
  const value = passwordInput.value;
  const hasLowercase = /[a-z]/.test(value);
  const hasUppercase = /[A-Z]/.test(value);
  const hasDigit = /\d/.test(value);
  const hasSpecial = /[@$]/.test(value);

  updateIndicator(lowercaseIndicator, hasLowercase);
  updateIndicator(uppercaseIndicator, hasUppercase);
  updateIndicator(digitIndicator, hasDigit);
  updateIndicator(specialIndicator, hasSpecial);
});

function updateIndicator(indicator, isValid) {
  if (isValid) {
    indicator.innerHTML = "&#10004;";
    indicator.classList.remove("invalid");
    indicator.classList.add("valid");
  } else {
    indicator.innerHTML = "&#10060;";
    indicator.classList.remove("valid");
    indicator.classList.add("invalid");
  }
}

document
  .getElementById("studentForm")
  .addEventListener("submit", function (event) {
    const password = passwordInput.value;
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$])[A-Za-z\d@$]{8,}$/;

    if (!passwordRegex.test(password)) {
      alert(
        "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character (@ or $)."
      );
      event.preventDefault();
    }
  });

phoneInput.addEventListener("input", function () {
  const value = phoneInput.value.trim();
  if (value.length > 10) {
    phoneError.style.display = "block";
  } else {
    phoneError.style.display = "none";
  }
});

phoneInput1.addEventListener("input", function () {
  const value = phoneInput1.value.trim();
  if (value.length > 10) {
    phoneError1.style.display = "block";
  } else {
    phoneError1.style.display = "none";
  }
});

document
  .getElementById("studentForm")
  .addEventListener("submit", function (event) {
    const phone = phoneInput.value.trim();
    const phone1 = phoneInput1.value.trim();
    if (phone.length !== 10) {
      phoneError.style.display = "block";
      event.preventDefault();
    }
    if (phone1.length !== 10) {
      phoneError1.style.display = "block";
      event.preventDefault();
    }
  });

document.getElementById('studentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/add_student', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Save the success message to sessionStorage
            sessionStorage.setItem('toastMessage', data.message);
            sessionStorage.setItem('toastType', 'success');
            
            console.log('Success message saved in sessionStorage');
            
            // Redirect to the admin dashboard
            window.location.href = "/admin_dashboard";
        } else {
            // Save the error message to sessionStorage
            sessionStorage.setItem('toastMessage', data.message);
            sessionStorage.setItem('toastType', 'error');
            
            console.log('Error message saved in sessionStorage');
            
            // Redirect to the admin dashboard or display error
            window.location.href = "/admin_dashboard";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});