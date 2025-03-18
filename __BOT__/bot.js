const chatbotIcon = document.getElementById('chatbot-icon');
const chatbotContainer = document.getElementById('chatbot-container');
const closeBtn = document.getElementById('close-btn');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');


chatbotIcon.addEventListener('click', () => {
    chatbotContainer.classList.toggle('active');
});

closeBtn.addEventListener('click', () => {
    chatbotContainer.classList.remove('active');
});


async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Append user's message
    appendMessage('user-message', message);
    userInput.value = '';

    // API integration with interface
    try {
        const response = await fetch('https://chatbotv5-s12s.onrender.com/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        // Append chatbot's response
        if (Array.isArray(data.response)) {
            appendMessage('bot-message', 'Saved Prompts:');
            data.response.forEach(prompt => {
                appendMessage('bot-message', `- ${prompt.prompt}`);
            });
        } else {
            appendMessage('bot-message', data.response || 'No response received');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('bot-message', 'Error communicating with the chatbot.');
    }
}

function appendMessage(className, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;

    // Use innerHTML instead of textContent to render HTML
    messageDiv.innerHTML = text;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});