#AI Document QA Bot

import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_URL = "https://router.huggingface.co/v1/chat/completions"
API_TOKEN = os.getenv("HF_TOKEN")

st.title("PDF text extractor")
pdf_file=st.file_uploader("Upload a pdf file",type=["pdf"])

if pdf_file is not None:
    pdf_reader=PyPDF2.PdfReader(pdf_file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()+"\n"
    
    st.subheader("Extracted text:")
    st.write(text)