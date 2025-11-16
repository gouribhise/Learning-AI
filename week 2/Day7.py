import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
HF_TOKEN=os.getenv("HF_TOKEN")
print("Get the 3 quotes on your favourite topic!")
subject=input("Enter the topic:")
url = "https://router.huggingface.co/v1/chat/completions"
payload={
      "model": "deepseek-ai/DeepSeek-V3-0324",
      "messages": [{"role": "user", "content": f"tell me 3 famous beautiful quotes on {subject}"}]
}

headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }


response = requests.post(url, json=payload, headers=headers)
data = response.json()

 
print("########################")  
print(data["choices"][0]["message"]["content"].strip())