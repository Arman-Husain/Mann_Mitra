import streamlit as st
import ollama
import time
import base64
import speech_recognition as sr  # For voice recognition
from textblob import TextBlob
import os

# Set up page layout and theme (MUST be the first Streamlit command)
st.set_page_config(page_title="AI Mental Healthcare Assistant", layout="wide")

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)
    return sentiment

def set_background(image_file):
    if not os.path.exists(image_file):
        st.warning(f"Background image '{image_file}' not found.")
        return
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    
    background_style = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Chat messages styling */
        .chat-message {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 12px;
            border-radius: 10px;
            margin: 5px 0;
            color: black;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        /* Animation for chat messages */
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: translateX(-50px); }}
            100% {{ opacity: 1; transform: translateX(0); }}
        }}
        /* Only apply animation to new messages */
        .new-message {{
            animation: fadeIn 1s ease-in-out;
        }}
        /* Button hover and click effects */
        button {{
            transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #5e72e4;
            transform: scale(1.05);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }}
        button:active {{
            transform: scale(1);
            box-shadow: 0px 0px 0px rgba(0, 0, 0, 0.2);
        }}
        /* Typing animation for AI messages */
        .typing-animation {{
            display: inline-block;
            animation: typing 1.5s steps(10) infinite;
        }}
        @keyframes typing {{
            0% {{ width: 0; }}
            100% {{ width: 100%; }}
        }}
        /* Hover effects for links */
        a:hover {{
            text-decoration: underline;
            color: #5e72e4;
        }}
        /* Main container padding and spacing */
        .stContainer {{
            padding: 20px;
        }}
        .stTextInput input {{
            font-size: 18px;
            padding: 12px;
            transition: border-color 0.3s ease;
        }}
        .stTextInput input:focus {{
            border-color: #5e72e4;
            outline: none;
        }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Set the background (Ensure "background.png" exists)
set_background("background.png")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About Chatbot")
    st.write("🧠 AI-powered assistant for mental health support.")
    st.write("💡 **Features:**")
    st.write("- ✅ Stress & Anxiety Management")
    st.write("- ✅ Self-care Tips")
    st.write("- ✅ Mindfulness Exercises")
    st.write("- ✅ Virtual Companion Chat")
    st.write("- ✅ Real-time Responses")
    st.write("- 🎙️ Voice Input Support")
    st.write("- 🎧 Voice Output Feature")

# Title & Introduction
st.title("🧠💙 AI Mental Healthcare Assistant")
st.write("👋 Welcome! Feel free to talk about your thoughts and emotions.")

# AI-Powered Daily Affirmations
daily_affirmations = {
    "😊 Happy": "Keep shining! Your positivity is contagious. 💛",
    "😔 Sad": "You're stronger than you think. This too shall pass. 💙",
    "😡 Angry": "Take a deep breath. You have control over your emotions. 🧘",
    "😰 Anxious": "Focus on the present. One step at a time. 🌿",
    "😴 Tired": "Rest is important. Listen to your body. 😌"
}

st.subheader("💬 Daily Affirmation")
mood = st.selectbox("How are you feeling today?", list(daily_affirmations.keys()), key="daily_affirmation_selectbox")
st.write(f"📢 **Affirmation:** {daily_affirmations[mood]}")

# Personalized Therapy Resources
therapy_resources = {
    "😊 Happy": ["Practice gratitude journaling 📝", "Listen to uplifting podcasts 🎧"],
    "😔 Sad": ["Write in a journal 🖊️", "Try a guided meditation 🧘"],
    "😡 Angry": ["Do breathing exercises 🌬️", "Engage in physical activity 🏃"],
    "😰 Anxious": ["Listen to calm music 🎶", "Try progressive muscle relaxation 💆"],
    "😴 Tired": ["Drink water & rest 💧", "Do light stretching 🏋️"]
}

st.subheader("🗂️ Personalized Therapy Resources")
st.write("🔹 Here are some recommendations for you:")
st.write("- " + therapy_resources[mood][0])
st.write("- " + therapy_resources[mood][1])

# Session state for chat history
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

# Function to generate AI response
def generate_response(user_input):
    """Handles AI response generation using Ollama API."""
    st.session_state["conversation_history"].append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3",
        messages=st.session_state["conversation_history"],
        stream=True,
        options={"max_tokens": 80}  # Keep responses concise
    )

    ai_response = ""
    response_box = st.empty()  # Placeholder for dynamic response updates

    for chunk in response:
        if "message" in chunk and "content" in chunk["message"]:
            text = chunk["message"]["content"]
            ai_response += text + " "
            response_box.markdown(f"<div class='chat-message new-message'><strong>🤖 AI:</strong> {ai_response}</div>", unsafe_allow_html=True)
            time.sleep(0.1)  # Simulating real-time response typing effect

    st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
    return ai_response

# Voice Recognition Function
def recognize_speech():
    """Uses speech recognition to convert spoken words to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Could not request results, please check your connection."
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again."

# Display chat history
st.subheader("📜 Chat History")
chat_container = st.container()

for msg in st.session_state["conversation_history"][-5:]:  # Show last 5 messages only
    role_icon = "👤" if msg["role"] == "user" else "🤖"
    with chat_container:
        # Static background for the existing messages, only new ones get animation
        st.markdown(f"<div class='chat-message'><strong>{role_icon} {msg['role'].capitalize()}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# User input field
user_message = st.text_input("💬 Type your thoughts or questions:", "", key="user_input")

# Voice Input Button
if st.button("🎙️ Speak Your Message"):
    user_message = recognize_speech()
    st.write(f"You said: {user_message}")
    if user_message and "conversation_history" in st.session_state:
        with st.spinner("🔍 Analyzing..."):
            ai_response = generate_response(user_message)

# Generate response when user provides input
if user_message and "conversation_history" in st.session_state:
    with st.spinner("🔍 Analyzing..."):
        ai_response = generate_response(user_message)

# Quick Questions Section
st.subheader("💡 Quick Questions:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😌 Stress Management"):
        generate_response("What are some effective ways to manage stress?")

with col2:
    if st.button("🧘 Mindfulness Tips"):
        generate_response("Can you guide me through a simple mindfulness exercise?")

with col3:
    if st.button("💙 Self-care Advice"):
        generate_response("What are some self-care tips for mental well-being?")