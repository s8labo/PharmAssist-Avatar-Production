from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your Azure Direct Line secret as an environment variable for security
DIRECTLINE_SECRET = os.environ.get("DIRECTLINE_SECRET")
GOOGLE_TTS_API_KEY = os.environ.get("GOOGLE_TTS_API_KEY")


@app.route('/get-token', methods=['GET'])
def get_token():
    if not DIRECTLINE_SECRET:
        return jsonify({"error": "Direct Line secret not configured."}), 500

    response = requests.post(
        "https://directline.botframework.com/v3/directline/tokens/generate",
        headers={"Authorization": f"Bearer {DIRECTLINE_SECRET}"}
    )

    if response.status_code == 200:
        token = response.json().get("token")
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Failed to get token", "details": response.text}), response.status_code


@app.route('/proxy-tts', methods=['POST'])
def proxy_tts():
    if request.method != 'POST':
        return jsonify({"error": "Method Not Allowed"}), 405

    if not GOOGLE_TTS_API_KEY:
        return jsonify({"error": "Google TTS API key not configured."}), 500

    try:
        data = request.get_json()
        tts_response = requests.post(
            f"https://eu-texttospeech.googleapis.com/v1beta1/text:synthesize?key={GOOGLE_TTS_API_KEY}",
            headers={'Content-Type': 'application/json'},
            json=data
        )
        print("tts_response", tts_response)
        return jsonify(tts_response.json()), tts_response.status_code
    except Exception as e:
        print("TTS Proxy Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443
    )
