import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import wikipedia
from gtts import gTTS
import os
import speech_recognition as sr

# --- WAKE WORD & BRAIN ---
def sam_speak(text):
    def play():
        try:
            tts = gTTS(text=text, lang='en')
            tts.save("speech.mp3")
            os.system("am start -a android.intent.action.VIEW -d file:///sdcard/speech.mp3 -t audio/mp3")
        except: pass
    threading.Thread(target=play).start()

def listen_for_wake_word():
    """Background loop that waits for 'Sam'"""
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            try:
                # Adjust for noise for 0.5 seconds for better mobile accuracy
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                
                if "sam" in text:
                    # Trigger the visual 'listening' feedback
                    root.after(0, lambda: start_sam_process("Yes? I'm listening!"))
            except:
                continue

def start_sam_process(msg):
    chat_display.config(state='normal')
    chat_display.insert('end', f"\n✨ {msg}\n", "sam_style")
    chat_display.config(state='disabled')
    sam_speak(msg)

def handle_chat():
    query = user_entry.get()
    if not query: return
    
    chat_display.config(state='normal')
    chat_display.insert('end', f"\n👤 You: {query}\n", "user_style")
    
    try:
        search_results = wikipedia.search(query)
        if search_results:
            # Fixed logic: search specifically for the title
            response = wikipedia.summary(search_results[0], sentences=2)
        else:
            response = "I couldn't find a specific match for that."
    except:
        response = "I'm having trouble connecting to my brain right now."

    chat_display.insert('end', f"👩‍💻 Sam: {response}\n", "sam_style")
    chat_display.config(state='disabled')
    chat_display.see('end')
    
    sam_speak(response)
    user_entry.delete(0, 'end')

# --- UI SETUP ---
root = tk.Tk()
root.title("Sam AI")
root.geometry("400x650")
root.configure(bg="#1e1e2e")

# Header with Photo
header = tk.Frame(root, bg="#27293d", pady=10)
header.pack(fill="x")
try:
    img = Image.open("sam.png") 
    img = img.resize((80, 80))
    sam_photo = ImageTk.PhotoImage(img)
    tk.Label(header, image=sam_photo, bg="#27293d").pack()
except:
    tk.Label(header, text="👩‍💻", font=("Arial", 40), bg="#27293d", fg="white").pack()

# Chat Window
chat_display = scrolledtext.ScrolledText(root, bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 11), state='disabled', bd=0)
chat_display.pack(padx=15, pady=10, fill="both", expand=True)
chat_display.tag_config("user_style", foreground="#89b4fa", font=("Arial", 11, "bold"))
chat_display.tag_config("sam_style", foreground="#a6e3a1")

# Input Area
input_frame = tk.Frame(root, bg="#1e1e2e", pady=15)
input_frame.pack(fill="x")

user_entry = tk.Entry(input_frame, bg="#313244", fg="white", font=("Arial", 12), bd=0)
user_entry.pack(side="left", padx=10, fill="x", expand=True, ipady=10)
user_entry.bind("<Return>", lambda e: handle_chat())

send_btn = tk.Button(input_frame, text="Ask", command=handle_chat, bg="#89b4fa", font=("Arial", 10, "bold"), bd=0, padx=10)
send_btn.pack(side="right", padx=10)

# Start Wake Word Listening in a separate background thread
threading.Thread(target=listen_for_wake_word, daemon=True).start()

root.mainloop()

