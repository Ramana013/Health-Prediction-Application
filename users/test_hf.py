# test_hf.py

import requests

API_KEY = ""

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(
    "https://huggingface.co/api/whoami-v2",
    headers=headers
)

print(response.status_code)
print(response.text)