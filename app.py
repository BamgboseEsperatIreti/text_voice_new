# app.py
# Free Text-to-Voice Generator with Password, Languages, Genders & UI

import streamlit as st
from gtts import gTTS
import tempfile

# -----------------------------
# PASSWORD PROTECTION
# Must be at the very top!
# -----------------------------
def check_password():
    """Returns True if user entered correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state.password_correct = True
            del st.session_state["password"]
        else:
            st.session_state.password_correct = False

    st.text_input(
        "🔒 Enter password to access this app",
        type="password",
        on_change=password_entered,
        key="password",
    )

    if "password_correct" in st.session_state and not st.session_state.password_correct:
        st.error("❌ Incorrect password")

    return False

if not check_password():
    st.stop()

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def generate_tts(text, lang="en", slow=False):
    """Generate speech from text using gTTS and save to temporary MP3 file."""
    tts = gTTS(text=text, lang=lang, slow=slow)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()
    return temp_file.name

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(
    page_title="🎙️ Free Text-to-Voice Generator",
    layout="centered"
)

st.title("🎙️ Free Text-to-Voice Generator")
st.write("CPU-friendly • Works Online • No API Key Needed")

# Sidebar for settings
with st.sidebar:
    st.header("Settings ⚙️")
    language = st.selectbox(
        "Select Language 🌐",
        options=["English", "Spanish", "German", "French"]
    )
    gender = st.radio(
        "Select Voice Gender 🗣️",
        options=["Male", "Female"]
    )
    speed = st.select_slider(
        "Voice Speed 🐢/⚡",
        options=["Slow", "Normal", "Fast"],
        value="Normal"
    )

# Map languages to gTTS codes
lang_map = {
    "English": "en",
    "Spanish": "es",
    "German": "de",
    "French": "fr"
}

# Map speed to gTTS slow parameter
speed_map = {
    "Slow": True,
    "Normal": False,
    "Fast": False
}

# Adjust slow flag based on language and gender
def get_slow_flag(language_choice, gender_choice, speed_choice):
    if language_choice == "English":
        return True if gender_choice == "Female" else speed_map[speed_choice]
    else:
        return speed_map[speed_choice]  # other languages: default voice

# -----------------------------
# Text Input
# -----------------------------
text_input = st.text_area(
    "Enter your text (up to 1000+ words):",
    height=220,
    placeholder="Paste your script here..."
)

# -----------------------------
# Generate Audio
# -----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    generate_btn = st.button("🎤 Generate Voice")

if generate_btn:
    if not text_input.strip():
        st.error("❌ Please enter some text.")
    else:
        try:
            with st.spinner("Generating voice... Please wait ⏳"):
                audio_path = generate_tts(
                    text=text_input,
                    lang=lang_map[language],
                    slow=get_slow_flag(language, gender, speed)
                )

            st.success("✅ Voice generated successfully!")

            # Play audio in browser
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")

            # Download button
            with col2:
                st.download_button(
                    "💾 Download Audio",
                    audio_bytes,
                    file_name="voice_output.mp3",
                    mime="audio/mp3"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
