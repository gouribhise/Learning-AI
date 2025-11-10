#Text summarizer
import requests
import json

url = "http://localhost:11434/api/chat"

prompt="Summarize the following paragraph in 3 lines:\n\n and save it in ai.txt" + """
Sure 🙂 — here’s a **10-line paragraph** on **Artificial Intelligence (AI):**

1. Artificial Intelligence (AI) is the branch of computer science that enables machines to think and act like humans.
2. It allows computers to learn from data, recognize patterns, and make decisions with minimal human input.
3. AI is used in everyday life through voice assistants, recommendation systems, and smart devices.
4. It helps industries automate tasks, improve efficiency, and reduce human error.
5. Machine learning and deep learning are key techniques that power modern AI systems.
6. AI can analyze massive amounts of information faster than humans ever could.
7. In healthcare, AI assists doctors in diagnosing diseases and personalizing treatments.
8. In transportation, it drives advancements in autonomous vehicles and traffic management.
9. However, AI also raises ethical concerns about privacy, bias, and job displacement.
10. As AI continues to evolve, it promises to transform the way we live, work, and connect with technology.

"""

data={
    "model":"phi3",
    "messages": [
        {"role": "user", "content":prompt}
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
    print("\n Summary:\n", full_reply)

with open("ai.txt","w",encoding="utf-8") as f:
    f.write(full_reply)

print("\n Saved summary to ai.txt")
