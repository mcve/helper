import requests

OPENAI_API_KEY = "ТВОЙ_KEY"

def transcribe(file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    files = {
        "file": open(file_path, "rb"),
        "model": (None, "whisper-1")
    }

    response = requests.post(url, headers=headers, files=files)

    return response.json()["text"]