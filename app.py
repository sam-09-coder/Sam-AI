
import streamlit as st
import wikipedia
from gtts import gTTS
import base64
from io import BytesIO
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="Sam AI", page_icon="🤖")

# --- SAM'S BRAIN (Search First Logic) ---
def get_sam_response(query):
    try:
        # Search for the best matching page title first
        search_results = wikipedia.search(query)
        if search_results:
            # Get the summary of the top search result (e.g., 'Narendra Modi')
            return wikipedia.summary(search_results[0], sentences=2)
        return "I couldn't find a specific match for that."
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=2)
    except:
        return "I'm having trouble connecting to my brain right now."

def get_voice_html(text):
    """Generates audio for Sam to speak"""
    tts = gTTS(text=text, lang='en')
    buffered = BytesIO()
    tts.write_to_fp(buffered)
    audio_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'

# --- SIDEBAR (Sam's Photo) ---
with st.sidebar:
    st.title("Sam AI")
    try:
        # Tries to load your photo
        img = Image.open("sam.png")
        st.image(img, width=150)
    except:
        st.write("👤 (Add sam.png to your folder to see my face!)")
    st.info("I'm online and ready to help!")

# --- MAIN CHAT UI ---
st.title("💬 Chat with Sam")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Sam's Smart Answer
    response = get_sam_response(prompt)
    
    # Show Sam's response
    with st.chat_message("assistant"):
        st.markdown(response)
        # Make Sam speak
        st.components.v1.html(get_voice_html(response), height=0)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

