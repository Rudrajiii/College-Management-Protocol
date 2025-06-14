document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.getElementById('flash-messages');
    setTimeout(() => {
        flashMessages.style.display = 'none';
    }, 3000);
});
