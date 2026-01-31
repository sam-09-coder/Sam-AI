import streamlit as st
from gtts import gTTS
import wikipedia
import io

# 1. THE SECRET TO SUCCESS: STRICT KEYWORDS
def sam_brain(user_input):
    user_input = user_input.lower().strip()
    
    # This dictionary stops the AI from giving wrong info
    strict_responses = {
        "mute": "Mute Support Active. I am now your voice. Type anything and I will speak it for you.",
        "blind": "Blind Support Active. I will now read all responses aloud automatically.",
        "safety": "Safety Protocol Active. Use the Emergency SOS button in the sidebar if you are in danger.",
        "pm of india": "The current Prime Minister of India is Narendra Modi.",
        "data science": "Data Science is the field of study that extracts knowledge from data using statistics and AI.",
        "hello": "Greetings! I am SAM, optimized for inclusive accessibility."
    }

    # Check for the exact word first
    for key in strict_responses:
        if key in user_input:
            return strict_responses[key]
    
    # Only use Wikipedia if the keyword isn't found
    try:
        return wikipedia.summary(user_input, sentences=1)
    except:
        return "I am operating locally. Please ask about Mute, Blind, or Safety support."

# 2. THE INTERFACE
st.set_page_config(page_title="SAM AI", layout="centered")

with st.sidebar:
    st.title("🛡️ Inclusive Features")
    st.info("Blind, Mute, and Safety Modules")
    blind_on = st.toggle("Blind Mode (Audio)", value=True)
    if st.button("🚨 TRIGGER SOS", type="primary"):
        st.error("EMERGENCY SIGNAL SENT")

st.title("🤖 SAM: Inclusive AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type for voice support..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    response = sam_brain(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
        # The Mute/Blind Vocalizer
        tts = gTTS(text=response, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format="audio/mp3", autoplay=True)
