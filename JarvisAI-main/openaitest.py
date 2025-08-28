import google.generativeai as genai
import pyttsx3
from config import apikey

genai.configure(api_key=apikey)

# Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("voice", engine.getProperty("voices")[1].id)

def say(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

model = genai.GenerativeModel("gemini-1.5-flash")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit", "bye"]:
        say("Goodbye!")
        break

    response = model.generate_content(query)
    answer = response.text
    say(answer)
