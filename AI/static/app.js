function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message === "") return;

    // Display the user's message in the chatbox
    appendMessage('You', message);

    // Send the message to the Flask backend
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the chatbot's response
        appendMessage('Bot', data.response);
    });

    // Clear the input box
    userInput.value = "";
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');

    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);

    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
// Function to check if the Enter key is pressed
function checkEnterKey(event) {
    if (event.keyCode === 13) {
        // Call sendMessage when Enter key is pressed
        sendMessage();
    }
}
function displayBotMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const botMessage = document.createElement('div');
    botMessage.classList.add('bot-message');
    chatBox.appendChild(botMessage);

    let i = 0;
    const interval = setInterval(() => {
        if (i < message.length) {
            botMessage.textContent += message.charAt(i);
            i++;
        } else {
            clearInterval(interval);  // Stop when all characters are displayed
        }

        // Scroll the chat box to the bottom to display the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 100); // Adjust speed (100ms per letter)
}