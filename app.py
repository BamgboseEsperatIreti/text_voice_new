# app.py
# FREE Offline Text-to-Voice Generator (CPU Friendly)

import streamlit as st
import pyttsx3
import tempfile
import os
from pydub import AudioSegment

# -----------------------------
# Helper Functions
# -----------------------------

def get_system_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    voice_list = []

    for v in voices:
        name = v.name.lower()
        gender = "Male"
        if "female" in name or "zira" in name or "hazel" in name:
            gender = "Female"
        voice_list.append({
            "id": v.id,
            "name": v.name,
            "gender": gender
        })

    return voice_list


def split_text(text, max_words=250):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks


def generate_audio_chunk(text, voice_id, rate):
    engine = pyttsx3.init()
    engine.setProperty("voice", voice_id)
    engine.setProperty("rate", rate)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_path = temp_file.name
    temp_file.close()

    engine.save_to_file(text, temp_path)
    engine.runAndWait()

    return temp_path


def generate_full_audio(text, voice_id, rate):
    chunks = split_text(text)
    audio_files = []

    for chunk in chunks:
        audio_path = generate_audio_chunk(chunk, voice_id, rate)
        audio_files.append(audio_path)

    combined_audio = AudioSegment.from_wav(audio_files[0])
    for audio in audio_files[1:]:
        combined_audio += AudioSegment.from_wav(audio)

    final_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    combined_audio.export(final_file.name, format="wav")

    # Cleanup temp chunks
    for f in audio_files:
        os.remove(f)

    return final_file.name

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Free Text-to-Voice Generator", layout="centered")
st.title("🎙️ Free Offline Text-to-Voice Generator")
st.write("CPU-friendly • No API • 100% Free • Works Offline")

text_input = st.text_area(
    "Enter your text (up to 1000+ words):",
    height=220,
    placeholder="Paste your script here..."
)

voices = get_system_voices()

gender_choice = st.radio("Select Voice Gender:", ["Male", "Female"])

filtered_voices = [v for v in voices if v["gender"] == gender_choice]

if not filtered_voices:
    st.warning("No voices found for this gender. Default voice will be used.")

voice_names = [v["name"] for v in filtered_voices]
voice_choice = st.selectbox("Select Voice:", voice_names if voice_names else ["Default"])

speed = st.select_slider(
    "Voice Speed:",
    options=["Slow", "Normal", "Fast"],
    value="Normal"
)

rate_map = {
    "Slow": 120,
    "Normal": 160,
    "Fast": 190
}

generate_btn = st.button("Generate Voice")

# -----------------------------
# Generate Audio
# -----------------------------

if generate_btn:
    if not text_input.strip():
        st.error("Please enter some text.")
    else:
        word_count = len(text_input.split())

        if word_count > 1000:
            st.info(f"Long text detected ({word_count} words). Audio will be generated in safe chunks.")

        try:
            with st.spinner("Generating voice... Please wait"):
                selected_voice_id = filtered_voices[voice_names.index(voice_choice)]["id"] if filtered_voices else pyttsx3.init().getProperty("voices")[0].id

                audio_path = generate_full_audio(
                    text_input,
                    selected_voice_id,
                    rate_map[speed]
                )

            st.success("Voice generated successfully!")

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/wav")

            st.download_button(
                "Download Audio",
                audio_bytes,
                file_name="voice_output.wav",
                mime="audio/wav"
            )

        except Exception as e:
            st.error(f"Error: {e}")
