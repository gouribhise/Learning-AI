import streamlit as st
import edge_tts
import asyncio
import tempfile

async def text_to_speech(text,voice="en-US-AriaNeural"):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as f:
        filename=f.name
    communicate=edge_tts.Communicate(text,voice)
    await communicate.save(filename)
    return filename

st.title("AI text to speech with edge tts")

text_input=st.text_area("Enter text:")

if st.button("Generate Speech:"):
    if text_input.strip()!="":
        st.info("Generating audio... please wait.")
        audio_file=asyncio.run(text_to_speech(text_input))
        audio_bytes=open(audio_file,"rb").read()
        st.audio(audio_bytes,format="audio/p3")
    else:
        st.warning("Please enter some text")
