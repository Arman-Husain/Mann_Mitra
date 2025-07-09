# AI Mental Healthcare Assistant

A Streamlit-based AI-powered chatbot for mental health support.  
This app provides daily affirmations, personalized therapy resources, and a conversational AI companion with both text and voice input.

## Features

- 🧠 AI-powered mental health assistant (Ollama + Llama3)
- 💬 Chat interface with conversation history
- 💡 Daily affirmations and mood-based therapy tips
- 🎙️ Voice input (speech-to-text)
- 📜 Quick access to stress management, mindfulness, and self-care advice
- 🎨 Custom background and modern UI

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/) (local LLM API)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/) (for microphone input)
- `background.png` image in the project folder

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/ai-mental-healthcare-assistant.git
    cd ai-mental-healthcare-assistant
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Download or place a `background.png` image in the project folder.**

4. **Start Ollama and ensure the `llama3` model is available:**
    ```sh
    ollama run llama3
    ```

5. **Run the app:**
    ```sh
    streamlit run app.py
    ```

## Usage

- Select your mood to get a daily affirmation and therapy tips.
- Type your thoughts or questions in the chat box, or use the 🎙️ button for voice input.
- Explore quick questions for instant advice on stress, mindfulness, and self-care.

## Notes

- Voice input requires a working microphone and PyAudio installed.
- Ollama must be running locally with the `llama3` model pulled.
- For best results, run locally (voice input may not work on remote servers).

## License

MIT License

---

*This project is for educational and supportive purposes only. It is not a substitute for professional mental health care.*