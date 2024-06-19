document.addEventListener("DOMContentLoaded", () => {
    const checkStatus = document.getElementById("Status");
    let defaultStatus = checkStatus.textContent; //?None
    const start_time = document.getElementById("start_time");
    const end_time = document.getElementById("end_time");
    console.log("Start time: " + start_time.value)
    console.log("end time: " + end_time.value);
    console.log("default status: " + defaultStatus); 
    const sumbit = document.getElementById("sumbit");
    console.log(sumbit);
    // Initialize socket connection to the specific URL
    var teacherSocket = io.connect('http://127.0.0.1:5000/teacher_dashboard');
    const form = document.getElementById('leaveApplicationForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent form submission

        // Get form values
        const enrollmentNumber = document.querySelector('input[name="enrollment"]').value;
        const startTime = document.getElementById('start_time').value;
        const endTime = document.getElementById('end_time').value;
        const reason = document.querySelector('input[name="reason"]').value;
        const status = 'Pending'; // Default status
        const Response = "accepted"; // Default Response



        try {
            // Send data to backend using fetch API or XMLHttpRequest
            // Update status display
            const statusSpan = document.getElementById('Status');
            statusSpan.textContent = 'Pending';

            const response = await fetch('/submit_application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    enrollment_number: enrollmentNumber,
                    start_time: startTime,
                    end_time: endTime,
                    reason: reason,
                    status: status,
                    Response:Response
                }),
            })
            .then(response => response.json())
            .then(data => {
            if (data.error) {
                showErrorAlert(data.error, 'error');
            }else{
                showSuccessAlert(data.message, 'success');
            }
        })
        teacherSocket.emit('apply', { message: 'Apply button clicked!' });

            

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to submit application');
            }
            const formData = new FormData(form);
            console.log(formData);
            const data = {};
            formData.forEach((value, key) => {
                    data[key] = value;
                });
            console.log(data);

            

            // Reset the form (optional)
            // form.reset();

            console.log('Application submitted successfully');

            // Send message to WebSocket server
            socket.send('New leave application submitted');
        } catch (error) {
            console.error('Error submitting application:', error);
            // Handle error as needed (e.g., show error message to user)
        }
    });

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
});



