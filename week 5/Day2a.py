#AI Document QA Bot
import requests
import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import pdfplumber


# Load .env file
load_dotenv()
API_URL = "https://router.huggingface.co/v1/chat/completions"
API_TOKEN = os.getenv("HF_TOKEN")

st.title("PDF QA Bot")
pdf_file=st.file_uploader("Upload a pdf file",type=["pdf"])

headers={
    "Authorization":f"Bearer {API_TOKEN}"
 }

pdf_text = ""

if pdf_file:
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text() + "\n"

question=st.text_input("Ask a question about pdf")

def get_answers(pdf_text,question):
    prompt=f"""
    You are a PDF QA answering assistant answer the quesion ONLY using
    the content from the given pdf text provided below.
     PDF TEXT: {pdf_text}
     QUESTION:{question}
     Answer:
     """


    payload = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.2
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return f"Error: {response.text}"

    #answer

if st.button("Get Answer"):
    if pdf_text=="":
        st.error("Upload a PDF first.")
    elif question.strip()=="":
        st.error("Please enter a question")
    else:
        answer=get_answers(pdf_text,question)
        st.subheader("Answer:")
        st.write(answer)