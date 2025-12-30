import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import os
import re
import subprocess
import psutil
import pyautogui
import wikipedia  # New Module for research
from google import genai

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyAZVMGEXXyIVsCMpUAcWlta3Ae9idN7t7U"
client = genai.Client(api_key=API_KEY)

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

def speak(text):
    cleaned_text = re.sub(r'[\*\-\#\_]', '', text)
    print(f"Jarvis: {cleaned_text}")
    engine = pyttsx3.init('sapi5')  
    voices = engine.getProperty('voices')
    for v in voices:
        if "India" in v.name:
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 185)
    engine.say(cleaned_text)
    engine.runAndWait()
    engine.stop()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n--- Systems Listening... ---")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio, language='en-in')
            print(f"You: {query}")
            return query.lower()
        except:
            return "none"

# --- 2. UTILITY FUNCTIONS ---

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12: speak("Good Morning, Yug Sir.")
    elif 12 <= hour < 18: speak("Good Afternoon, Yug Sir.")
    else: speak("Good Evening, Yug Sir.")
    speak("Jarvis is online. How can I assist your research today?")

def take_screenshot():
    speak("Taking a screenshot, Sir.")
    name = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
    pyautogui.screenshot().save(name)
    speak(f"Saved as {name}.")

def system_health():
    battery = psutil.sensors_battery()
    cpu = psutil.cpu_percent()
    speak(f"Sir, power is at {battery.percent} percent and CPU usage is {cpu} percent.")

def open_browser(query):
    site = query.replace("open", "").replace("jarvis", "").strip()
    url = f"https://www.{site}.com" if "." not in site else f"https://{site}"
    for path in CHROME_PATHS:
        if os.path.exists(path):
            speak(f"Opening {site}, Sir.")
            subprocess.Popen([path, url])
            return
    webbrowser.open(url)

# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
    wish_me()
    
    while True:
        query = listen()

        if "jarvis" in query:
            query = query.replace("jarvis", "").strip()

            # --- NEW: WIKIPEDIA SEARCH ---
            if "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip()
                try:
                    # Fetches a 2-sentence summary
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia...")
                    speak(results)
                except Exception as e:
                    speak("Sir, I couldn't find a specific entry for that.")

            # --- SYSTEM COMMANDS ---
            elif "system status" in query or "battery" in query:
                system_health()

            elif "screenshot" in query:
                take_screenshot()

            elif "open notepad" in query:
                subprocess.Popen(["notepad.exe"])

            # --- WEB COMMANDS ---
            elif "open" in query:
                open_browser(query)

            elif "search" in query:
                term = query.replace("search for", "").replace("search", "").strip()
                speak(f"Searching Google for {term}.")
                webbrowser.open(f"https://www.google.com/search?q={term}")

            # --- UTILITIES ---
            elif "time" in query:
                speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}, Sir.")

            elif "exit" in query or "stop" in query:
                speak("Goodbye, Yug Sir. Systems offline.")
                break

            # --- GEMINI AI BRAIN ---
            elif query != "none":
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash", contents=f"User: {query}")
                    speak(res.text)
                except:
                    speak("Core connection error, Sir.")