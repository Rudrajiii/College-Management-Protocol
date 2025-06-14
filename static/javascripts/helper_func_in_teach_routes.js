console.log("JavaScript file loaded successfully.");
/**
 * Function to delete a teacher from the system
 * @param {string} userId - The ID of the teacher to delete
 */
function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this teacher? This action cannot be undone.')) {
        fetch(`/delete_user/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to delete teacher');
                });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || 'Teacher deleted successfully!');
            
            window.location.reload();
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
            console.error('Delete error:', error);
        });
    }
}

function updateUser(userId) {
    window.location.href = `/update_a_staff?id=${userId}`;
}
function showMore(userId) {
    window.location.href = `/teacher_profile/${userId}`;
}