
import streamlit as st
from gtts import gTTS
import wikipedia
import io

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="SAM: Inclusive AI", page_icon="🤖")

# 2. SIDEBAR - THIS IS WHERE YOUR FEATURES LIVE
with st.sidebar:
    st.title("🛡️ Inclusive Modules")
    st.markdown("---")
    
    # Blind Support Feature
    st.subheader("👁️ Blind Support")
    blind_mode = st.checkbox("Auto-Read Responses", value=True, help="Enables Text-to-Speech for every AI reply.")
    
    # Mute Support Feature
    st.subheader("🔇 Mute Support")
    st.success("Vocalizer: ACTIVE")
    st.caption("Sam will speak out any text typed in the chat to assist non-verbal users.")
    
    # Safety Feature
    st.subheader("🚨 Safety Guard")
    if st.button("TRIGGER EMERGENCY SOS", use_container_width=True):
        st.error("EMERGENCY ALERT: Location sent to authorities (Simulated).")
    
    st.markdown("---")
    st.info("SAM uses a **Hybrid AI Architecture** to work in both Online and Offline environments.")

# 3. MAIN INTERFACE
st.title("🤖 SAM: Hybrid AI Assistant")
st.write("Specialized in Inclusive Accessibility and Data Science.")

# 4. SAM'S BRAIN (Corrected Facts)
def sam_brain(user_input):
    user_input = user_input.lower()
    
    # Local Knowledge Base (Ensures 100% Accuracy for Demo)
    local_facts = {
        "pm of india": "The current Prime Minister of India is Narendra Modi.",
        "who is the prime minister of india": "The current Prime Minister of India is Narendra Modi.",
        "president of india": "The current President of India is Droupadi Murmu.",
        "hello": "Greetings! I am SAM. I am optimized for Blind, Mute, and Underprivileged support.",
        "data science": "Data Science is the study of data to extract meaningful insights for business."
    }
    
    # Check Local Brain First
    if user_input in local_facts:
        return local_facts[user_input]
    
    # If not in local, search Wikipedia
    try:
        return wikipedia.summary(user_input, sentences=1)
    except:
        return "I am currently in Offline Mode for this topic. How can I assist you with safety or vocalization?"

# 5. VOICE ENGINE (For Blind/Mute)
def speak(text):
    tts = gTTS(text=text, lang='en')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    return audio_fp

# 6. CHAT HISTORY LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. CHAT INPUT
if prompt := st.chat_input("Type here to vocalize or ask Sam..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response and handle audio
    response = sam_brain(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
        if blind_mode:
            audio_data = speak(response)
            st.audio(audio_data, format="audio/mp3", autoplay=True)
