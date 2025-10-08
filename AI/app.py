from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import time
import json
import random
from flask_cors import CORS
import google.generativeai as genai

# =========
# Setup
# =========
load_dotenv()

app = Flask(__name__)
# Allow your GitHub Pages domain (adjust if you host elsewhere)
CORS(app, origins=['https://qnity001.github.io'])

API_KEY = os.getenv("API_KEY", "").strip()
if not API_KEY:
    raise RuntimeError("Missing API_KEY env var.")

# Pick endpoint: prefer global; optionally set GEMINI_REGION to `us-central1` or `europe-west1`
GEMINI_REGION = os.getenv("GEMINI_REGION", "").strip().lower()

def pick_api_endpoint(region: str) -> str:
    allowed = {"us-central1", "europe-west1"}
    if region in allowed:
        return f"{region}-generativelanguage.googleapis.com"
    return "generativelanguage.googleapis.com"  # global default (avoids accidental zero-quota regions)

API_ENDPOINT = pick_api_endpoint(GEMINI_REGION)

# Prevent inherited envs from forcing a bad region (e.g., us-south1)
for bad in ("GOOGLE_CLOUD_REGION", "CLOUDSDK_COMPUTE_REGION", "GOOGLE_CLOUD_QUOTA_LOCATION"):
    if os.getenv(bad, "").strip().lower() == "us-south1":
        os.environ.pop(bad, None)

# Configure Gemini SDK
genai.configure(
    api_key=API_KEY,
    client_options={"api_endpoint": API_ENDPOINT}
)

# Files
DATA_FILE = "data.json"
SYSTEM_INSTRUCTION_FILE = "system_instruction.txt"

# =========
# Utilities
# =========
def load_system_instruction(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback empty instruction
        return ""

system_instruction = load_system_instruction(SYSTEM_INSTRUCTION_FILE)

def load_history() -> list:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Corrupt file fallback
        return []

def save_history(history: list) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def trim_history(history: list, max_turns: int = 16) -> list:
    """
    Keep only the last `max_turns*2` entries (user+model per turn) to prevent runaway tokens.
    Adjust as needed.
    """
    return history[-(max_turns * 2):] if len(history) > max_turns * 2 else history

# Simple exponential backoff for transient 429/5xx (won’t fix zero-quota regions)
def with_retry(call_fn, max_retries=2, base=0.8):
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return call_fn()
        except Exception as e:
            msg = str(e)
            # If error explicitly says quota limit value is 0 -> don't retry
            if "quota_limit_value" in msg and '"0"' in msg:
                last_exc = e
                break
            # Retry only on 429/5xx-ish
            if any(code in msg for code in ("429", "503", "500", "unavailable", "deadline")) and attempt < max_retries:
                sleep_s = base * (2 ** attempt) + random.uniform(0, 0.4)
                time.sleep(sleep_s)
                last_exc = e
                continue
            last_exc = e
            break
    if last_exc:
        raise last_exc

# =========
# Routes
# =========
@app.route("/")
def index():
    # Expect a templates/bot.html (same as your original)
    return render_template("bot.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    if not user_message:
        return jsonify({"response": "Please provide a non-empty message.", "history": []}), 400

    # Load & trim global history
    conversation_history = trim_history(load_history(), max_turns=16)

    # Model configuration
    generation_config = {
        "temperature": 1.0,           # dial back from 1.35 for stability
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 300,
        "response_mime_type": "text/plain",
    }

    # Build model
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        generation_config=generation_config,
        system_instruction=system_instruction,
        tools="code_execution",
    )

    # Append user turn
    conversation_history.append({"role": "user", "parts": [{"text": user_message}]})

    # Small cooldown to reduce bursts
    time.sleep(0.3)

    try:
        chat_session = model.start_chat(history=conversation_history)

        def _send():
            return chat_session.send_message(user_message)

        response = with_retry(_send, max_retries=2, base=0.8)
        response_text = getattr(response, "text", "").strip() or "(No content returned.)"

        # Append model turn & persist
        conversation_history.append({"role": "model", "parts": [{"text": response_text}]})
        save_history(conversation_history)

        return jsonify({"response": response_text, "history": conversation_history})

    except Exception as e:
        # Bubble up actionable hints if we detect zero-quota region
        msg = str(e)
        hint = ""
        if "quota_location" in msg and "us-south1" in msg:
            hint = " Hint: your calls are hitting us-south1 which has 0 quota. Set GEMINI_REGION=us-central1 or use the global endpoint (default)."
        return jsonify({"response": f"Error: {msg}{hint}", "history": conversation_history}), 500

# =========
# Main
# =========
if __name__ == "__main__":
    # Tip:
    #   API_KEY=... GEMINI_REGION=us-central1 python app.py
    # or just set API_KEY and leave GEMINI_REGION unset to use the global endpoint.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
