// Sample data
// const cardData = {
//     imgSrc: "https://images.unsplash.com/photo-1527980965255-d3b416303d12?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxNDU4OXwwfDF8cmFuZG9tfHx8fHx8fHx8MTY0Mzk4NjU1Mw&ixlib=rb-1.2.1&q=80&w=200",
//     name: "David Grant",
//     skill: "3D artist",
//     rating: "4.7 Rating",
//     reviews: "4,447 Reviews",
//     students: "478 Students",
//     description: "john_doe is a passionate elementary school teacher dedicated to fostering a nurturing and stimulating classroom environment. With over eight years of experience, she excels in creating engaging lesson plans that cater to diverse learning styles. Her commitment to student growth is evident in her interactive teaching methods and personalized approach to education."
// };

// Function to create a user card
// Function to create a user card
function createUserCard(data) {
    const card = document.createElement('div');
    card.className = 'user-card';

    card.innerHTML = `
        <span class="avatar-holder">
            <img src="${data.profile_pic}" alt="Avatar">
        </span>
        <span class="user-info-holder">
            <h2 class="name">${data.username}</h2>
            <span class="skill">${data.bio}</span>

            <div class="evaluations">
                <span class="stars evaluation">
                    <span class="star-icon evaluation-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                            <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
                        </svg>
                    </span>
                    <span class="star-text evaluation-text">${data.rating} Rating</span>
                </span>

                <span class="reviews evaluation">
                    <span class="reviews-icon evaluation-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-award" viewBox="0 0 16 16">
                            <path d="M9.669.864 8 0 6.331.864l-1.858.282-.842 1.68-1.337 1.32L2.6 6l-.306 1.854 1.337 1.32.842 1.68 1.858.282L8 12l1.669-.864 1.858-.282.842-1.68 1.337-1.32L13.4 6l.306-1.854-1.337-1.32-.842-1.68L9.669.864zm1.196 1.193.684 1.365 1.086 1.072L12.387 6l.248 1.506-1.086 1.072-.684 1.365-1.51.229L8 10.874l-1.355-.702-1.51-.229-.684-1.365-1.086-1.072L3.614 6l-.25-1.506 1.087-1.072.684-1.365 1.51-.229L8 1.126l1.356.702 1.509.229z"/>
                            <path d="M4 11.794V16l4-1 4 1v-4.206l-2.018.306L8 13.126 6.018 12.1 4 11.794z"/>
                        </svg>
                    </span>
                    <span class="reviews-text evaluation-text">${data.reviews} Reviews</span>
                </span>

                <span class="student evaluation">
                    <span class="student-icon evaluation-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                            <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                        </svg>
                    </span>
                    <span class="student-text evaluation-text">${data.teaches_total_students} Students</span>
                </span>
            </div>

            <span class="desc">
                <p>${data.description}</p>
            </span>

            <span class="button">
            <button class="show-more-btn">
            <a style="text-decoration:none;" href="/teacher_profile/${data._id}">Show More</a>
            </button>
            <button class="show-more-btn">
            <a style="text-decoration:none;" href="/update_a_staff?id=${data._id}">Update Info</a>
            </button>
            <button class="show-more-btn"  onclick="deleteUser('${data._id}')">
            <a style="text-decoration:none;" href="">Delete</a>
            </button>
            </span>
        </span>
    `;

    return card;
}

function deleteUser(userId) {
    if (confirm("Are you sure you want to delete this staff?")) {
        fetch(`/delete_user/${userId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                alert("User deleted successfully.");
                location.reload();
            } else {
                alert("Failed to delete user.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    }
}


// Function to display cards
function displayCard(data) {
    const cardContainer = document.getElementById('card-container');
    const card = createUserCard(data);
    cardContainer.appendChild(card);
}

// Fetch data from the backend and display cards
fetch('http://127.0.0.1:5000/teachers_data')
    .then(response => response.json())
    .then(data => {
        data.forEach(teacher => displayCard(teacher));
    })
    .catch(error => console.error('Error fetching teachers data:', error));
