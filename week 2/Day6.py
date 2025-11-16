import requests
import json
import textwrap
from itertools import zip_longest
from dotenv import load_dotenv
load_dotenv()
import os
HF_TOKEN=os.getenv("HF_TOKEN")
 
 
def wrap(text, width=50):
    return textwrap.fill(text, width=width).split("\n")

 
def get_ollama_reply():
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "phi3",
        "messages": [{"role": "user", "content": "tell me fun fact about space"}]
    }
    full_reply = ""
    with requests.post(url, json=data, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                part = json.loads(line.decode("utf-8"))
                if "message" in part and "content" in part["message"]:
                    full_reply += part["message"]["content"]
                elif part.get("done"):
                    break
    return full_reply.strip()


 
def get_hf_reply():
    HF_TOKEN = os.getenv("HF_TOKEN")
    url = "https://router.huggingface.co/v1/chat/completions"

    payload = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [{"role": "user", "content": "tell me fun fact about space"}]
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    print("\n=== HF RAW RESPONSE ===")
    print(data)           
    print("======================\n")

  
    if "choices" not in data:
        raise Exception(f"HuggingFace error: {data}")

    return data["choices"][0]["message"]["content"].strip()

 
    url = "https://router.huggingface.co/v1/chat/completions"

    payload = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [{"role": "user", "content": "tell me fun fact about space"}]
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


 
ollama_text = get_ollama_reply()
hf_text = get_hf_reply()

 
ollama_lines = wrap(ollama_text, 55)
hf_lines = wrap(hf_text, 55)

 
print("\n" + "=" * 130)
print("🟦 OLLAMA (phi3)".ljust(60) + " | " + "🟨 HUGGINGFACE (DeepSeek-V3)")
print("=" * 130)

for left, right in zip_longest(ollama_lines, hf_lines, fillvalue=""):
    print(left.ljust(60) + " | " + right)
