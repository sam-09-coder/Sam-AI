
import streamlit as st
from gtts import gTTS
import wikipedia
import io

# --- MODERN GEMINI-STYLE UI ---
st.set_page_config(page_title="SAM: Inclusive AI", page_icon="🤖")

st.title("🤖 SAM: Hybrid Inclusive AI")
st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INCLUSIVE FEATURES LOGIC ---
def sam_brain(user_input):
    user_input = user_input.lower()
    
    # Offline/Local Intent Mockup
    intents = {
        "hello": "Greetings! I am SAM, optimized for Blind, Mute, and Underprivileged support.",
        "data science": "Data Science is the field of study that combines domain expertise, programming skills, and knowledge of mathematics and statistics to extract meaningful insights from data.",
        "safety": "Safety protocol active. (Note: Mobile sensors like accelerometers require native app permissions not available in standard browsers)."
    }
    
    if user_input in intents:
        return intents[user_input]
    
    try:
        # Online Brain (Wikipedia)
        return wikipedia.summary(user_input, sentences=2)
    except:
        return "I am operating in local mode. Please ask about 'Data Science' or 'Safety'."

# --- VOICE OUTPUT (For Blind/Mute Support) ---
def speak(text):
    tts = gTTS(text=text, lang='en')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    return audio_fp

# --- CHAT INPUT ---
if prompt := st.chat_input("Type here to vocalize or ask Sam..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Sam's Response
    response = sam_brain(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
        # Auto-play audio for the Blind/Mute
        audio_data = speak(response)
        st.audio(audio_data, format="audio/mp3", autoplay=True)
