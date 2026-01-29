import streamlit as st
import wikipedia
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
import base64

# --- WEB PAGE CONFIG ---
st.set_page_config(page_title="Sam AI Assistant", page_icon="🤖")
st.title("🤖 Meet Sam")
st.markdown("I can look up facts, show pictures, and tell you the weather!")

# --- SAM'S VOICE FUNCTION (WEB VERSION) ---
def get_sam_voice_html(text):
    tts = gTTS(text=text, lang='en')
    buffered = BytesIO()
    tts.write_to_fp(buffered)
    # Convert audio to a format the browser can play
    audio_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'

# --- THE USER INTERFACE ---
user_input = st.text_input("Ask Sam something (or type a city for weather):")

if user_input:
    # 1. Handle Weather
    if "weather" in user_input.lower():
        city = st.text_input("Which city specifically?", key="city_input")
        if city:
            report = requests.get(f"https://wttr.in/{city}?format=3").text.strip()
            st.info(report)
            st.components.v1.html(get_sam_voice_html(f"The weather in {city} is {report}"), height=0)

    # 2. Handle Facts & Images
    else:
        try:
            # Get Info
            summary = wikipedia.summary(user_input, sentences=2)
            st.success(summary)
            
            # Show Image
            page = wikipedia.page(user_input)
            if page.images:
                img_url = page.images[0]
                st.image(img_url, caption=f"An image of {user_input}")
            
            # Sam Speaks
            st.components.v1.html(get_sam_voice_html(summary), height=0)
            
        except:
            st.error("Sam couldn't find that topic. Try being more specific!")
		