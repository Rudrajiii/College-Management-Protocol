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
});

