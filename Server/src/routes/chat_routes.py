import json

from flask import Blueprint, request, jsonify
import requests
from http import HTTPStatus

CHAT_URL = '/api/chat'

# Define the blueprint
chat_bp = Blueprint('chat', __name__, url_prefix=CHAT_URL)

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@chat_bp.route('/send', methods=['POST'])  # Use POST instead of GET
def send_message():
    try:
        # Retrieve JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), HTTPStatus.BAD_REQUEST

        print(f'Received message request: {data}')

        # Validate required fields
        prompt = data.get('prompt')
        context = data.get('context')

        if not prompt:
            return jsonify({"error": "Missing 'prompt' in request"}), HTTPStatus.BAD_REQUEST
        if not context:
            return jsonify({"error": "Missing 'context' in request"}), HTTPStatus.BAD_REQUEST

        print(f'Sending message: {prompt}')
        print(f'Sending context: {context}')

        content = f"System prompt: You are a helpfull assistant\nContext: {context}\nPrompt: {prompt}"

        # Prepare the payload for Ollama API
        payload = {
            "model": "deepseek-r1:1.5b",  # Replace with your desired model
            "prompt": content,
            "stream": False,
        }

        # Send the request to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)
        print(response.text)

        if response.status_code == 200:
            # Parse the response JSON
            text = response.text
            data = json.loads(text)
            print(data)
            res = data.get('response')
            print(res)

            return jsonify({"response": res}), HTTPStatus.OK

    except requests.RequestException as e:
        # Handle errors related to the Ollama API request
        return jsonify({"error": f"Ollama API error: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"error": f"Unexpected error: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

