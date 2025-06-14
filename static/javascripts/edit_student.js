// elements accessing :-
const phoneInput = document.getElementById('contact');
const phoneError = document.getElementById('phoneBug');

const parentsPhone = document.getElementById('parentsContact');
const parentsPhoneError = document.getElementById('parentsPhoneBug');

const userInput = document.getElementById('userInput');
const message = document.getElementById('message');

const passwordInput = document.getElementById('passwordInput');
const passwordText = document.querySelector('.passwordText');

// encoding functions :-

// user ph no 
 phoneInput.addEventListener('input', function(event) {
  event.preventDefault();
  const value = phoneInput.value.trim();

  if(value.length === 10) {
      phoneError.textContent = "Recorded Characters";
      phoneError.style.color = "green";
  } else {
      phoneError.textContent = "Un-Recorded Characters";
      phoneError.style.color = "red";
  }
 })

// parents ph no   
 parentsPhone.addEventListener('input', function(event) {
  event.preventDefault();
  const value = parentsPhone.value.trim();

  if(value.length === 10) {
          parentsPhoneError.textContent = "Recorded Characters";
          parentsPhoneError.style.color = "green";
  } else {               
          parentsPhoneError.textContent = "Un-Recorded Characters";
          parentsPhoneError.style.color = "red";
  }
 })

 // username 
  userInput.addEventListener('input', function(event) {
     event.preventDefault();

     const username = userInput.value.trim();
     const userPattern = /^[a-zA-Z][a-zA-Z0-9_]{5,19}$/;
     
     if(userPattern.test(username)) {
      message.textContent = "Username is valid!";
      message.style.color = "green";
     } else {
      message.textContent = "Username is invalid!";
      message.style.color = "red";
     }
  });           

  // password

   passwordInput.addEventListener('input', function(event) {
      event.preventDefault();

      const password = passwordInput.value.trim();
      const isValidPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      
      if(isValidPassword.test(password)) {
          passwordText.textContent = "Looks strong!";
          passwordText.style.color = "green";
      } else {
          passwordText.textContent = "Please match the below criteria!";
          passwordText.style.color = "red";
      }

   })
