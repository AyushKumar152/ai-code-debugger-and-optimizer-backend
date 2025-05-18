from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)



JUDGE0_API_URL = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true"
JUDGE0_API_KEY = os.getenv("RAPIDAPI_KEY")
JUDGE0_API_HOST = os.getenv("RAPIDAPI_HOST")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openai/gpt-3.5-turbo"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return "Server is running. Use /run, /debug, or /optimize."

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    source_code = data.get('source_code')
    language_id = data.get('language_id')

    headers = {
        'Content-Type': 'application/json',
        'X-RapidAPI-Key': JUDGE0_API_KEY,
        'X-RapidAPI-Host': JUDGE0_API_HOST
    }

    payload = {
        'source_code': source_code,
        'language_id': language_id,
    }

    try:
        response = requests.post(JUDGE0_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": str(http_err), "details": response.text}), response.status_code
    except Exception as err:
        return jsonify({"error": "Unexpected server error", "details": str(err)}), 500

@app.route('/debug', methods=['POST'])
def debug_code():
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')

    prompt = f"Debug this {language} code and explain the issue:\n\n{code}"

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": f"You are an expert {language} debugger."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=OPENROUTER_HEADERS, json=payload, timeout=10)
        response_data = response.json()

        print("OpenRouter Debug Response:", response_data)

        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0]["message"]["content"]
            return jsonify({"result": result})
        else:
            return jsonify({"result": "No debugging suggestions returned by the AI."})
    except Exception as e:
        return jsonify({"error": "Debugging failed", "details": str(e)}), 500

@app.route('/optimize', methods=['POST'])
def optimize_code():
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')

    prompt = f"Optimize this {language} code for performance and readability:\n\n{code}"

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": f"You are an expert {language} optimizer."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=OPENROUTER_HEADERS, json=payload, timeout=10)
        response_data = response.json()

        print("OpenRouter Optimize Response:", response_data)

        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0]["message"]["content"]
            return jsonify({"result": result})
        else:
            return jsonify({"result": "No optimization suggestions returned by the AI."})
    except Exception as e:
        return jsonify({"error": "Optimization failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
