import requests
import json

url = "http://localhost:11434/api/chat"
data = {
    "model": "phi3",
    "messages": [
        {"role": "user", "content": "Tell me a fun fact about space!"}
    ]
}

# Stream the response properly
with requests.post(url, json=data, stream=True) as resp:
    full_reply = ""
    for line in resp.iter_lines():
        if line:
            # Each line is its own JSON object
            part = json.loads(line.decode("utf-8"))
            if "message" in part and "content" in part["message"]:
                full_reply += part["message"]["content"]
            elif part.get("done"):
                break
    print("\nAI says:", full_reply)
