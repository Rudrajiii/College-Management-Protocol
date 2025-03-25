document.addEventListener('DOMContentLoaded', () => {
    // Connect to the admin dashboard namespace
    var adminSocket = io.connect('http://127.0.0.1:5000/admin_dashboard');

    adminSocket.on('alert', function(data) {
      showSuccessAlert(data.message); 
    });

    function showSuccessAlert(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'success-alert';
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);
    setTimeout(() => {
      alertDiv.remove();
    }, 3000);
  }
  window.addEventListener('DOMContentLoaded', function() {
          const toastMessage = sessionStorage.getItem('toastMessage');
          const toastType = sessionStorage.getItem('toastType');

  
          console.log('Toast message retrieved:', toastMessage);
          console.log('Toast type retrieved:', toastType);

  
          if (toastMessage) {
              showToast(toastMessage, toastType);
              // Clear the message from sessionStorage after showing
              sessionStorage.removeItem('toastMessage');
              sessionStorage.removeItem('toastType');
          }
      });
  
      function showToast(message, type) {
          console.log('Showing toast...');
          
          const successToast = document.querySelector('.success-toast');
          const failureToast = document.querySelector('.failure-toast');
          
          if (type === 'success') {
              successToast.innerText = message;
              successToast.style.display = 'block'; 
              failureToast.style.display = 'none'; 
          } else if (type === 'error') {
              failureToast.innerText = message;
              failureToast.style.display = 'block'; 
              successToast.style.display = 'none'; 
          }

          // Display for 5 seconds
          setTimeout(() => {
              if (type === 'success') {
                  successToast.style.display = 'none'; 
                  console.log('Hiding the success toast...');
              } else if (type === 'error') {
                  failureToast.style.display = 'none'; 
                  console.log('Hiding the failure toast...');
              }
          }, 5000); 
      }
});

