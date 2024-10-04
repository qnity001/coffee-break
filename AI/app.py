from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure the Gemini AI SDK with the API key
genai.configure(api_key=os.getenv('API_KEY'))  # Ensure 'API_KEY' matches the name in your .env file

# Function to load system instruction from a text file with utf-8 encoding
def load_system_instruction(file_path):
    """Loads system instruction from a text file with utf-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Load the system instruction from the text file
system_instruction = load_system_instruction('system_instruction.txt')

# Route for the homepage
@app.route('/')
def chat():
    return render_template('Chat.html')

# Route to get a response from Gemini AI
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')

    # Create the model with configuration and safety settings
    generation_config = {
        "temperature": 1.35,        # Adjusts randomness; higher = more random
        "top_p": 0.95,              # Nucleus sampling; considers the top 95% probable tokens
        "top_k": 64,                # Considers the top 64 tokens
        "max_output_tokens": 300,   # Limits the number of tokens in the output
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=system_instruction,  # Load the instruction from the file
        tools='code_execution',
    )

    # Start a chat session with an empty or predefined history for context
    chat_session = model.start_chat(
        history=[]  # You can load a predefined history here if needed
    )

    # Generate a response based on the user's input
    try:
        response = chat_session.send_message(user_message)
        print(response._result)
        print(response.text)
        # Extract and format the response
        response_text = response.text

    except Exception as e:
        # Handle any errors that occur during the API request
        response_text = f"Error: {str(e)}"

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
