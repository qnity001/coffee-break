function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message === "") return;

    // Display the user's message in the chatbox
    appendMessage('You', message);

    // Send the message to the Flask backend
    fetch('https://coffee-break.onrender.com/get_response', {
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

    if (sender === 'You') {
       messageElement.classList.add('user-message'); 

                
        const userName = document.createElement('div');
        userName.classList.add('user-name');
        userName.innerHTML = "You";
        messageElement.appendChild(userName);

        const userContent = document.createElement('div');
        userContent.classList.add('user-content');
        userContent.innerHTML = message;
        messageElement.appendChild(userContent);

    } else 
    {
        messageElement.classList.add('bot-message');

        // div for avatar of the mascot
        const botImage = document.createElement('div');
        botImage.classList.add('bot-image');
        botImage.innerHTML = "<img src=\"https://github.com/qnity001/coffee-break/blob/main/coffee/Mascot.png?raw=true\" alt=\"mascot\">";
        messageElement.appendChild(botImage);

        // div for the bot's text
        const botText = document.createElement('div');
        botText.classList.add('bot-text');
        messageElement.appendChild(botText);

        // div for bot's name
        const botName = document.createElement('div');
        botName.classList.add('bot-name');
        botName.innerHTML = "Milo";
        botText.appendChild(botName);

        // div for bot's message
        const botContent = document.createElement('div');
        botContent.classList.add('bot-content');
        botContent.innerHTML = message;
        botText.appendChild(botContent);
    }
    
    chatBox.appendChild(messageElement);
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
