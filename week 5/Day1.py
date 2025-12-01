#AI Travel Itinerary Generator

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_URL = "https://router.huggingface.co/v1/chat/completions"
API_TOKEN = os.getenv("HF_TOKEN")
 
headers={
    "Authorization":f"Bearer {API_TOKEN}"
 }

def get_itinerary(location):
    payload = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [
            {"role": "user", "content": f"Create a 3-day travel itinerary for {location} in bullet points."}
        ],
        "max_new_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    # Extract text
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error parsing response: {e}\nFull response: {data}"


st.title("AI Travel Itinerary Generator")
st.write("Enter any location, and get a 3-day travel plan!")

location=st.text_input("Enter a location:",value="Goa")

if st.button("Generate Itinerary"):
    if location.strip()=="":
        st.warning("Please enter a location")
    else:
        with st.spinner("Generating AI itinerary..."):
            itinerary=get_itinerary(location)
        st.subheader(f"3-Day Itinerary for{location}")
        st.text(itinerary)

# streamlit run Day1.py