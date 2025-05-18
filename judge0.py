import requests

JUDGE0_API_URL = "https://ce.judge0.com/submissions/?base64_encoded=false&wait=true"

def run_code(source_code, language_id):
    payload = {
        "source_code": source_code,
        "language_id": language_id
    }

    response = requests.post(JUDGE0_API_URL, json=payload)
    return response.json()
