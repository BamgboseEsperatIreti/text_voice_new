# app.py
# Free Online Text-to-Voice Generator (Cloud Compatible)

import streamlit as st
from gtts import gTTS
import tempfile

# -----------------------------
# Helper Functions
# -----------------------------

def generate_tts(text, lang="en"):
    """
    Generate speech from text using gTTS and save to a temporary MP3 file.
    Returns the path to the MP3 file.
    """
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()
    return temp_file.name

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Free Text-to-Voice Generator", layout="centered")
st.title("🎙️ Free Text-to-Voice Generator")
st.write("CPU-friendly • No API key • Works Online")

# Text input
text_input = st.text_area(
    "Enter your text (up to 1000+ words):",
    height=220,
    placeholder="Paste your script here..."
)

# Voice speed
speed = st.select_slider(
    "Voice Speed:",
    options=["Slow", "Normal", "Fast"],
    value="Normal"
)

# Map speed to approximate gTTS 'slow' parameter
# gTTS only supports slow=True or False, so we approximate:
# Slow -> slow=True, Normal/Fast -> slow=False
slow_map = {
    "Slow": True,
    "Normal": False,
    "Fast": False
}

generate_btn = st.button("Generate Voice")

# -----------------------------
# Generate Audio
# -----------------------------

if generate_btn:
    if not text_input.strip():
        st.error("Please enter some text.")
    else:
        try:
            with st.spinner("Generating voice... Please wait"):
                # Generate audio using gTTS
                audio_path = generate_tts(text_input)

            st.success("Voice generated successfully!")

            # Play audio in browser
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3")

            # Download button
            st.download_button(
                "Download Audio",
                audio_bytes,
                file_name="voice_output.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"Error: {e}")
