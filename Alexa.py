



import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pywhatkit


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "API error. Please check your internet connection."


def execute_command(command):
    if "hello" in command:
        response = "Hello! How can I help you?"
    elif "time" in command:
        response = f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif "open google" in command:
        response = "Opening Google..."
        webbrowser.open("https://www.google.com")
    elif "play" in command:
            response = "playing the song "+command
            pywhatkit.playonyt(command)
    else:
        response = "Sorry, I don't know that command."

    speak(response)
    print("Assistant:", response)


if __name__ == "__main__":
    speak("Voice Assistant Activated. How can I help you?")
    while True:
        command = listen()
        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        execute_command(command)
