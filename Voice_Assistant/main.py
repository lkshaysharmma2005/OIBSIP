from dotenv import load_dotenv
import speech_recognition as sr
import webbrowser
import pyttsx3
from googleapiclient.discovery import build
import threading
import requests
import os

# Load API keys from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("CSE_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API
YOUTUBE = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ---------- Utility Functions ----------
def speak(text, block=True):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    if block:
        engine.say(text)
        engine.runAndWait()
    else:
        threading.Thread(target=lambda: (engine.say(text), engine.runAndWait())).start()

def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CSE_ID}"
    response = requests.get(url).json()
    if "items" in response:
        return response["items"][0]["link"]
    return None

def search_youtube(query):
    request = YOUTUBE.search().list(q=query, part="snippet", type="video", maxResults=1)
    response = request.execute()
    video_id = response["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"

# ---------- Command Processor ----------
def process_command(command):
    c = command.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open github" in c:
        webbrowser.open("https://github.com")

    elif "open linkedin" in c:
        webbrowser.open("https://www.linkedin.com/in/lakshay-sharma-3986b7327")

    elif c.startswith("play "):  # play <song/video>
        song = c.replace("play", "", 1).strip()
        if song:
            link = search_youtube(song)
            speak(f"Playing {song} on YouTube...")
            webbrowser.open(link)
        else:
            speak("Tell me what should I play!")

    elif c.startswith("search "):  # search <query>
        query = c.replace("search", "", 1).strip()
        if query:
            link = google_search(query)
            if link:
                speak(f"Here’s what I found for {query}")
                webbrowser.open(link)
            else:
                speak("Sorry, I couldn’t find anything.")
        else:
            speak("What should I search?")

    else:
        speak("I didn’t understand that command.")

# ---------- Main Loop ----------
if __name__ == "__main__":
    speak("Initializing Personal Voice Assistant...")

    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)

            word = recognizer.recognize_google(audio).lower()
            print("Recognized:", word)

            if "hello" in word:  # wake word
                speak("Yes sir, I’m listening.")
                print("Assistant Active...")

                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                process_command(command)

        except Exception as e:
            print("Error:", e)
