document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Handle new application notification from server
    socket.on('new_application', (data) => {
        // Handle the notification (e.g., show a notification to admin)
        alert(`New application received:\n${JSON.stringify(data, null, 2)}`);
    });
});