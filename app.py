# app_web.py
# Free Text-to-Voice Generator for Streamlit Cloud (gTTS) with Donations and Character Count

import streamlit as st
from gtts import gTTS
import tempfile

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
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("Settings ⚙️")
    language = st.selectbox(
        "Select Language 🌐",
        options=["English", "Spanish", "German", "Italian", "French"]
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
    "Italian": "it",
    "French": "fr"
}

# Map speed to gTTS slow parameter
speed_map = {
    "Slow": True,
    "Normal": False,
    "Fast": False  # gTTS does not support fast, so normal is used
}

# -----------------------------
# Text Input
# -----------------------------
text_input = st.text_area(
    "Enter your text (up to 5000 characters):",
    height=220,
    placeholder="Paste your script here..."
)

# -----------------------------
# Character / Word Count
# -----------------------------
num_chars = len(text_input)
num_words = len(text_input.split())
st.markdown(f"📝 Characters: {num_chars} | Words: {num_words}")

if num_chars > 5000:
    st.warning("⚠️ Text is very long! For best results, keep under 5000 characters (~800 words).")

# -----------------------------
# Generate Audio
# -----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    generate_btn = st.button("🎤 Generate Voice")

if generate_btn:
    if not text_input.strip():
        st.error("❌ Please enter some text.")
    elif num_chars > 5000:
        st.error("❌ Text exceeds the recommended 5000 characters. Please shorten it.")
    else:
        try:
            with st.spinner("Generating voice... Please wait ⏳"):
                audio_path = generate_tts(
                    text=text_input,
                    lang=lang_map[language],
                    slow=speed_map[speed]
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

st.markdown("---")

# -----------------------------
# Donation Section
# -----------------------------
st.subheader("💖 Support this project")
st.markdown(
    """
If you enjoy using this app and want to support me, you can donate via **Ko-fi** or **PayPal**.  
Your support helps me keep improving the app and adding more languages and features!

<div style="display:flex; gap:10px;">
<a href="https://ko-fi.com/sp_solutions" target="_blank">
    <button style="padding:10px 20px; font-size:16px;">Donate via Ko-fi</button>
</a>
<a href="https://www.paypal.com/donate/?hosted_button_id=QYF89E88GFAYN" target="_blank">
    <button style="padding:10px 20px; font-size:16px;">Donate via PayPal</button>
</a>
</div>
""", unsafe_allow_html=True
)
