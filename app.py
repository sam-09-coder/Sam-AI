
import streamlit as st
import wikipedia
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO
from gtts import gTTS
import base64

# --- INITIALIZE SESSION STATE (The Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CONFIG ---
st.set_page_config(page_title="Sam AI", page_icon="👩‍💻")

# Change this to your local image file name, e.g., "sam.jpg"
SAM_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712139.png"

def get_sam_voice_html(text):
    """Makes Sam speak"""
    try:
        tts = gTTS(text=text, lang='en')
        buffered = BytesIO()
        tts.write_to_fp(buffered)
        audio_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    except: return ""

def get_image(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            return results[0]['image'] if results else None
    except: return None

# --- UI LAYOUT ---
st.title("👩‍💻 Sam AI Assistant")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=SAM_AVATAR if message["role"] == "assistant" else None):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# User Input Box
if prompt := st.chat_input("Say something to Sam..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- SAM'S BRAIN (LOGIC) ---
    response_text = ""
    extra_image = None

    if "show me" in prompt.lower():
        query = prompt.lower().replace("show me", "").strip()
        extra_image = get_image(query)
        response_text = f"Here is what I found for {query}."
        
    elif "weather" in prompt.lower():
        city = prompt.lower().split("in")[-1].strip() if "in" in prompt.lower() else "London"
        response_text = requests.get(f"https://wttr.in/{city}?format=3").text.strip()
        
    else:
        try:
            response_text = wikipedia.summary(prompt, sentences=2)
        except:
            response_text = "I'm listening! I can tell you about facts, weather, or show you images."

    # Add Sam's response to history
    full_response = {"role": "assistant", "content": response_text}
    if extra_image:
        full_response["image"] = extra_image
    
    st.session_state.messages.append(full_response)

    # Display Sam's response
    with st.chat_message("assistant", avatar=SAM_AVATAR):
        st.markdown(response_text)
        if extra_image:
            st.image(extra_image)
        # Trigger Voice
        st.components.v1.html(get_sam_voice_html(response_text), height=0)
