#Audio to text
import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import os

st.title("🎙️ Offline Speech-to-Text (Whisper Local)")

@st.cache_resource
def load_model():
    return WhisperModel("small", device="cpu", compute_type="int8")

model = load_model()

audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path)

    with st.spinner("Transcribing locally..."):
        segments, info = model.transcribe(tmp_path)

        text = ""
        for seg in segments:
            text += seg.text + " "

    st.subheader("Transcription:")
    st.write(text)

 
    os.remove(tmp_path)
