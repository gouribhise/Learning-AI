# Text summarizer using Ollama
import requests
import json

url = "http://localhost:11434/api/chat"

# Take user input
prompt = input("Enter a paragraph: ")

# Prepare the payload
data = {
    "model": "phi3",
    "messages": [
        {
            "role": "user",
            "content": f"Summarize the following paragraph in 1 to 2 lines only:\n\n{prompt}"
        }
    ]
}

# Send request and stream response
full_reply = ""
with requests.post(url, json=data, stream=True) as resp:
    for line in resp.iter_lines():
        if not line:
            continue
        part = json.loads(line.decode("utf-8"))
        if "message" in part and "content" in part["message"]:
            print(part["message"]["content"], end="", flush=True)  # Live output
            full_reply += part["message"]["content"]
        if part.get("done"):
            break

# Print and save the final summary
print("\n\nSummary:\n", full_reply)

with open("ai.txt", "w", encoding="utf-8") as f:
    f.write(full_reply)

print("\n💾 Saved summary to ai.txt")
