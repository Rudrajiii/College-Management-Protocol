document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#clear_msg').forEach(button => {
      button.addEventListener('click', (event) => {
        const liElement = event.target.closest('li');
        const status = liElement.querySelector('.status').textContent.split(': ')[1];
  
        if (status.trim() === 'Pending') {
            showErrorAlert('Cannot clear notification while status is pending.');
          //!error sending...
        } else {
          const applicationId = liElement.dataset.id;
          fetch(`/delete_notification/${applicationId}`, {
            method: 'DELETE',
          })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                liElement.remove();
                showSuccessAlert('Notification cleared successfully.');
                //*success sending...
              } else {
                showErrorAlert('Failed to clear notification.');
                //!error sending...
              }
            });
        }
      });
    });
  
    document.querySelectorAll('.accept-button').forEach(button => {
      button.addEventListener('click', () => updateStatus(button, 'Accepted'));
    });
  
    document.querySelectorAll('.reject-button').forEach(button => {
      button.addEventListener('click', () => updateStatus(button, 'Rejected'));
    });
  
    function updateStatus(button, newStatus) {
      const liElement = button.closest('li');
      const applicationId = liElement.dataset.id;
  
      fetch(`/update_status/${applicationId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            liElement.querySelector('.status').textContent = `Current Status: ${newStatus}`;
            showUpdateAlert(`Application ${newStatus}`);
          } else {
            alert('Failed to update status.');
          }
        });
    }

    function showErrorAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'error-alert';
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        setTimeout(() => {
          alertDiv.remove();
        }, 3000);
      }
    function showSuccessAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'success-alert';
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        setTimeout(() => {
          alertDiv.remove();
        }, 3000);
      }
    function showUpdateAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'update-alert';
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        setTimeout(() => {
          alertDiv.remove();
        }, 3000);
      }
  });


