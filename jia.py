import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random

# ==================== SPEECH ENGINE SETUP ====================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Everybody, Welcome to Our Mini Project!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Everybody, Welcome to Our Mini Project!")
    else:
        speak("Good Evening Everybody, Welcome to Our Mini Project!")
    speak("I am jia. This project is developed by Jaithrini and Neha. Please tell me how may I help you.")

# ==================== ONLINE SPEECH RECOGNITION ====================
def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        speak("I didn't hear anything. Please try again.")
        return "none"

    try:
        print("Recognizing using Google (Online)...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said (Online): {query}\n")
        return query.lower()

    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return "none"

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return "none"

# ==================== EMAIL FUNCTION ====================
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jaithrini12@gmail.com', 'zfqp ssjg jlpy pmqe') 
    server.sendmail('jaithrini12@gmail.com', to, content)
    server.close()

# ==================== OTHER FEATURES ====================
def calculator(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
        print(f"Result: {result}")
    except Exception as e:
        speak("Sorry, I could not calculate that.")
        print(f"Error: {e}")

def writeNote(note):
    with open("notes.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {note}\n")
    speak("Note has been written.")

def readNotes():
    if os.path.exists("notes.txt"):
        with open("notes.txt", "r") as f:
            notes = f.read()
            print(notes)
            speak(notes)
    else:
        speak("You don't have any notes yet.")

# ==================== MAIN FUNCTION ====================
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if query == "none":
            continue 
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=1)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I could not find that on Wikipedia.")

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")

        elif 'play music' in query:
            music_dir = r"C:\Users\JAITHRINI\Music"
            songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
            if songs:
                song_to_play = random.choice(songs)
                os.startfile(os.path.join(music_dir, song_to_play))
            else:
                speak("Sorry, I could not find any music files.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codePath = r"C:\Users\JAITHRINI\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
            os.startfile(codePath)

        elif 'send mail' in query:
            try:
                speak("What should I send?")
                content = takeCommand()
                if content != "none":
                    to = "jaithrini12@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send the email.")

        elif 'calculate' in query:
            speak("Tell me the expression.")
            expression = takeCommand()
            if expression != "none":
                calculator(expression)

        elif 'write a note' in query:
            speak("What should I write?")
            note = takeCommand()
            if note != "none":
                writeNote(note)

        elif 'read note' in query:
            readNotes()

        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Okay, bye!")
            break
