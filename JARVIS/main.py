from dotenv import load_dotenv
import speech_recognition as sr
import webbrowser
import pyttsx3
from googleapiclient.discovery import build
import threading 
import os

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def speak(text, block=True):
    print(text)
    engine = pyttsx3.init()  # reinitialize each time
    if block:
        engine.say(text)
        engine.runAndWait()
    else:
        # ✅ Run speaking in background so listening doesn't wait
        threading.Thread(target=lambda: (engine.say(text), engine.runAndWait())).start()


def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open linkdin" in c.lower():
        webbrowser.open("https://www.linkedin.com/in/lakshay-sharma-3986b7327")
    # elif c.lower().startswith("play"):
    #     song = c.lower().split(" ")[1]
    #     if len(song) > 1:
    #         link = musicplayer.music[song]
    #         webbrowser.open(link)
    #     else:
    #         ("Tell me what should i play!")

YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

def search_youtube(query):
    request = YOUTUBE.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=1
    )
    response = request.execute()
    video_id = response["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"

# # Example
# song = "Imagine Dragons Believer"
# link = search_youtube(song)
# webbrowser.open(link)

        

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)

            word = r.recognize_google(audio)
            print("Recognized:", word)

            if word.lower() == "jarvis":
                speak("yes sir")
                print("Jarvis Active...")
                with sr.Microphone() as source:
                    
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                if command.lower().startswith("play"):
                    song = command.replace("play", "").strip()
                    if command.lower().startswith("play"):
                        song = command.replace("play", "", 1).strip()
                        if len(song) == 0:
                            speak("Tell me what should I play!")
                        else:
                            link = search_youtube(song)
                            webbrowser.open(link)

                else:
                    processcommand(command)
                    

        except Exception as e:
            print("error:", e)
   