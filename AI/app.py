import flask
from flask import request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load API key and .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Path for conversation history file
history_file = "data.json"

# Load conversation history from file
def load_history():
    try:
        with open(history_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save conversation history to file
def save_history(history):
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)

# Initialize the conversation history (load from file)
conversation_history = load_history()

# Create the generation model configuration
generation_config = {
    "temperature": 0.98,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

######################################################################################################
#########                                Flask initiation                                   ##########
######################################################################################################

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

# Function to format the conversation history to the expected format
def format_history_for_gemini(history):
    formatted_history = []
    for entry in history:
        formatted_history.append({
            "role": entry["role"],  # Must be either 'user' or 'model'
            "parts": [{"text": entry["content"]}]  # Correct structure using 'parts' and 'text'
        })
    return formatted_history

@app.route('/query', methods=['POST'])
def query_gemini():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config
    )

    # Format the conversation history for Gemini
    formatted_history = format_history_for_gemini(conversation_history)

    # Start a chat session and include the formatted conversation history
    try:
        chat_session = model.start_chat(
            history=formatted_history  # Use the formatted history
        )
    except Exception as e:
        print(f"Error starting chat session: {e}")
        return jsonify({'error': 'Error starting chat session'}), 500

    # Send the user's query and receive the AI response
    try:
        response = chat_session.send_message(query)

        if response.text:
            # Add the current query and response to the conversation history
            conversation_history.append({"role": "user", "content": query})  # User's input
            conversation_history.append({"role": "model", "content": response.text})  # AI's response

            # Save the updated conversation history to file
            save_history(conversation_history)

            return jsonify({'response': response.text})
        else:
            return jsonify({'error': 'No valid response from Gemini AI'}), 500

    except Exception as e:
        print(f"Error during send_message: {e}")
        return jsonify({'error': 'Error during send_message'}), 500

if __name__ == '__main__':
    app.run(debug=True)
