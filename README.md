Jarvis A.I — Personal Voice Assistant 🤖✨

A powerful, friendly, voice-driven personal assistant built with Python, Gemini (Google Generative AI), speech recognition, and TTS.
Perfect for opening websites, answering questions, playing local audio, and running simple voice-driven automations — all with a warm Jarvis-style personality. 🚀🎧

🔥 Features

🎙️ Speech-to-Text (ASR) using speech_recognition.

🗣️ Text-to-Speech (TTS) using gTTS (and optional pyttsx3).

🧠 AI-powered answers with Google Generative AI (Gemini).

🎵 Play music/audio with pygame and subprocess.

🧵 Thread-safe TTS queue to prevent overlapping speech.

💬 Chat memory support for contextual conversations.

⚡ Ready-to-run examples: jarvis_main.py (voice assistant) & openaitest.py (console version).

📁 Project Structure
.
├── jarvis_main.py       # Main voice assistant  
├── openaitest.py        # Console test script  
├── config.py            # Stores your API key  
├── requirements.txt     # Dependencies  
├── README.md            # Project documentation  
└── .gitignore

🛠️ Requirements

SpeechRecognition  
pygame  
gTTS  
google-generativeai  
pyttsx3  
pyaudio  

🚀 Setup & Installation

1.Clone the repo

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2.Add your API key
Create a file config.py in the project root:

apikey = "YOUR_GOOGLE_GENERATIVE_AI_API_KEY"

3.Run Jarvis

python main.py

Or run the console test:

python openaitest.py

🧭 How to Use

Start the assistant → It says: “Jarvis A.I ready to assist you”.

Speak commands like:

🔗 “Open YouTube” → Opens YouTube in browser.

⏰ “What’s the time?” → Tells the current time.

💡 “Tell me something” → AI-powered response.

🧹 “Reset chat” → Clears conversation history.

📴 “Jarvis quit” / “Quit” → Shuts down gracefully.

💡 Troubleshooting

🎤 Microphone issues?

Check OS microphone permissions.

Adjust energy_threshold in code.

🔊 PyAudio installation error (Windows)

pip install pipwin
pipwin install pyaudio

🎶 TTS playback issues

Uses temporary MP3s; Windows may lock files briefly — retry logic included.

⚠️ Gemini API errors

Verify API key in config.py.

Check internet connection and API quota.

🌟 Future Improvements

🎤 Add wake-word detection (e.g., “Hey Jarvis”).

🖥️ Build a GUI (Tkinter/React/Electron).

🗓️ Add reminders & calendar integration.

🔗 Integrate with external APIs (weather, news, etc.).

⚡ Enable streaming responses for faster replies.

🔐 Security

Never commit your API key.

Add config.py to .gitignore.

Jarvis is your personal A.I assistant — ready to help with voice commands, automation, and smart AI answers.
This project is a great base to experiment, customize, and expand into your own futuristic assistant. 🚀💙

Enjoy building — Jarvis at your service! 🤖⚡


