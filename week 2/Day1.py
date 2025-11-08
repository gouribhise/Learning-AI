from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Get API key from .env file
api_key = os.getenv("API_KEY")

# Define API endpoint and headers
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",  # ✅ Use f-string in Python
    "Content-Type": "application/json"
}

# Define the data payload
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello AI, tell me a fun fact about space!"}
    ]
}

# Send POST request
response = requests.post(url, headers=headers, json=data)

# Parse and print the AI's response
#print(response.json()["choices"][0]["message"]["content"])
print(response.json())
