import requests

from dotenv import load_dotenv
load_dotenv()
import os
HF_TOKEN=os.getenv("HF_TOKEN")

url = "https://router.huggingface.co/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-V3-0324",
    "messages": [
        {"role": "user", "content": "Tell me something about Pune city."}
    ]
}

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("STATUS:", response.status_code)
print("RAW:", response.text)

data = response.json()
print("\nAI:", data["choices"][0]["message"]["content"])
