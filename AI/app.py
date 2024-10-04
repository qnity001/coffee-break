from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time
import json
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the Gemini AI SDK with the API key
genai.configure(api_key=os.getenv('API_KEY'))

# Path to the data.json file for global conversation history
DATA_FILE = 'data.json'

# Function to load system instruction from a text file with utf-8 encoding
def load_system_instruction(file_path):
    """Loads system instruction from a text file with utf-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Load the system instruction from the text file
system_instruction = load_system_instruction('system_instruction.txt')

# Helper function to load conversation history from data.json
def load_history():
    """Load the conversation history from data.json."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)  # Return the global conversation history
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty history

# Helper function to save conversation history to data.json
def save_history(history):
    """Save the conversation history to data.json."""
    with open(DATA_FILE, 'w') as file:
        json.dump(history, file, indent=4)

# Route for the homepage
@app.route('/')
def index():
    return render_template('bot.html')

# Route to get a response from Gemini AI with global history stored in data.json
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')

    # Load the global conversation history from the data.json file
    conversation_history = load_history()

    # Create the model with configuration and safety settings
    generation_config = {
        "temperature": 1.35,        # Adjusts randomness; higher = more random
        "top_p": 0.95,              # Nucleus sampling; considers the top 95% probable tokens
        "top_k": 64,                # Considers the top 64 tokens
        "max_output_tokens": 300,   # Limits the number of tokens in the output
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=system_instruction,  # Load the instruction from the file
        tools='code_execution',
    )

    # Append the new user message to the conversation history
    conversation_history.append({'role': 'user', 'parts': [{'text': user_message}]})

    # Introduce a cool-down period (for example, 2 seconds)
    time.sleep(2)

    # Generate a response based on the user's input and the entire history
    try:
        chat_session = model.start_chat(history=conversation_history)  # Pass the global history to the chat model
        response = chat_session.send_message(user_message)
        response_text = response.text

        # Append the model's response to the conversation history
        conversation_history.append({'role': 'model', 'parts': [{'text': response_text}]})

        # Save the updated conversation history to the data.json file
        save_history(conversation_history)

    except Exception as e:
        # Handle any errors that occur during the API request
        response_text = f"Error: {str(e)}"

    # Return the response and updated history to the client
    return jsonify({'response': response_text, 'history': conversation_history})

if __name__ == '__main__':
    app.run(debug=True)