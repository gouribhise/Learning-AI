#Chat with your own AI bot!
import requests
import json

def AI_Chat(question):
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "phi3",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, json=data, stream=True, timeout=30)

        if response.status_code == 200:
            print("AI:", end=" ")
            try:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        if "message" in data and "content" in data["message"]:
                            print(data["message"]["content"], end="", flush=True)
            except KeyboardInterrupt:
                 print("\n Response interrupted.")
            print()  
        else:
            print("Error:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("Connection error:", e)


# Chat loop
while True:
    try:
        q = input("\nYou: ")
        if q.lower() in ["exit", "quit", "bye", "exit()"]:
            print("Goodbye!!!")
            break
        else:
            AI_Chat(q)
    except KeyboardInterrupt:
        print("\n(Type 'exit' to quit)")
        continue
