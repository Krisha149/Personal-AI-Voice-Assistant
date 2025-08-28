import os
import webbrowser
import datetime
import subprocess
import threading
import queue
import tempfile
import time

import speech_recognition as sr
import pygame
from gtts import gTTS
import google.generativeai as genai

# ========= CONFIG =========
from config import apikey  
MODEL_NAME = "gemini-1.5-flash"
WAKE_PROMPT_EN = "Jarvis A.I ready to assist you"

# ========= GEMINI SETUP =========
genai.configure(api_key=apikey)
model = genai.GenerativeModel(MODEL_NAME)

# ========= TTS ENGINE (gTTS + pygame + queue) =========
class SpeechEngine:
    def __init__(self):
        # Initialize pygame mixer once
        pygame.mixer.init()
        self.q = queue.Queue()
        self.lock = threading.Lock()  # protect stop/flush
        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()

    def _run(self):
        while True:
            text = self.q.get()
            if text == "__EXIT__":
                break
            try:
                self._speak_blocking(text)
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.q.task_done()

    def _speak_blocking(self, text: str):
        # Generate mp3 to a temp file
        # (generate path first to avoid Windows file lock races)
        fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        try:
            tts = gTTS(text=text, lang="en")
            tts.save(temp_path)

            # Play audio
            with self.lock:
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.05)

        finally:
            # robust remove with retry (Windows sometimes lags)
            for _ in range(5):
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    break
                except PermissionError:
                    time.sleep(0.05)

    def say(self, text: str):
        print("Jarvis:", text)
        self.q.put(text)

    def say_once(self, text: str):
        # Flush queue + stop current, then say the latest only
        with self.lock:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        with self.q.mutex:
            self.q.queue.clear()
        self.say(text)

    def stop(self):
        self.say_once("")  # stop current
        self.q.put("__EXIT__")
        self.worker.join(timeout=2)


speech = SpeechEngine()

def say(text: str):
    speech.say(text)

def say_once(text: str):
    speech.say_once(text)

# ========= ASR =========
def takeCommand():
     # wait until Jarvis has finished speaking
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    r.energy_threshold = 300
    with sr.Microphone() as source:
        # audio = r.listen(source, phrase_time_limit=5)
        try:
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except Exception:
            say_once("Some Error Occurred. Sorry from Jarvis")
            return ""

# ========= CHAT MEMORY =========
chatStr = ""

def ai_with_history(prompt: str):
    global chatStr
    chatStr += f"User: {prompt}\nJarvis: "
    try:
        response = model.generate_content(chatStr)
        answer = response.text
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        print("AI Error:", e)
        return None

def ai_simple(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("AI Error:", e)
        return None

# ========= MAIN APP =========
if __name__ == "__main__":
    print("Welcome to Jarvis A.I")
    say_once(WAKE_PROMPT_EN)

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"],
        ["instagram", "https://www.instagram.com"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://www.stackoverflow.com"],
        ["gmail", "https://mail.google.com"],
        ["reddit", "https://www.reddit.com"],
        ["twitter", "https://www.twitter.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["netflix", "https://www.netflix.com"],
        ["prime video", "https://www.primevideo.com"],
        ["spotify", "https://www.spotify.com"],
    ]

    try:
        while True:
            # print("Listening...")
            query = takeCommand()
            if not query:
                # say_once("Please say something")
                continue

            q_lower = query.lower()

            # ----- Site handling (avoid double-speak) -----
            handled = False
            for site in sites:
                trigger = f"open {site[0]}"
                if trigger in q_lower:
                    say_once(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    handled = True
                    break
            if handled:
                continue

            # ----- Local commands -----
            if "open music" in q_lower:
                musicPath = "E:/Excelsior/super_dash/assets/audio/background.mp3"
                subprocess.run(["start", "", musicPath], shell=True)
                say_once("Playing your music")
                continue

            if "the time" in q_lower:
                hour = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                say_once(f"Sir time is {hour} bajke {minute} minutes")
                continue

            if "reset chat" in q_lower:
                chatStr = ""
                say_once("Chat memory cleared")
                continue

            if "jarvis quit" in q_lower or "quit" in q_lower:
                say_once("Shutting down. Goodbye Krisha!")
                break

            # ----- AI response (single, clean speak) -----
            answer = ai_simple(query)
            if answer is None:
                # say a friendly line
                say_once("Sorry, I cannot answer right now.")
            else:
                say_once(answer)

    finally:
        speech.stop()
