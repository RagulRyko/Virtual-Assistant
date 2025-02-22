import speech_recognition as sr
import pyttsx3
import datetime
import calendar
import requests
import pywhatkit as kit

# Initialize the speech engine
engine = pyttsx3.init()


class VirtualAssistant:
    def __init__(self):
        self.name = "Assistant"
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Convert text to speech."""
        engine.say(text)
        engine.runAndWait()

    def listen(self):
        """Listen to audio and return the recognized text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I did not understand. Could you repeat that?")
            return None
        except sr.RequestError:
            self.speak("Sorry, I am having trouble connecting to the internet.")
            return None

    def get_time(self):
        """Return current time and date."""
        now = datetime.datetime.now()
        day_of_week = calendar.day_name[now.weekday()]
        time = now.strftime("%H:%M:%S")
        return f"Today is {day_of_week}, and the time is {time}."

    def get_weather(self,city):
        """Fetch weather information."""
        api_key = "1d50fe7f28e954e67b2c65fd8e2dd9c6"  # Replace with your OpenWeatherMap API key
        # city = "India"  # You can change the city here or ask the user for it
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return "Sorry, I couldn't fetch the weather right now."

        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The current temperature in {city} is {temperature}°C with {weather_description}"

    def play_song(self, song_name):
        """Play a song on YouTube using pywhatkit."""
        try:
            self.speak(f"Playing {song_name} on YouTube.")
            kit.playonyt(song_name)  # pywhatkit function to play on YouTube
        except Exception as e:
            self.speak("Sorry, I couldn't play the song. Please try again.")
            print(e)

    def perform_task(self, task):
        """Perform different tasks based on user input."""
        if 'time' in task:
            self.speak(self.get_time())
        elif 'weather' in task:
            # Asking for the city if the user says "weather"
            self.speak("Please tell me the city.")
            city_name = self.listen()
            if city_name:
                self.speak(self.get_weather(city_name))  # Call the weather method with the city name
            else:
                self.speak("I couldn't hear the city name. Please try again.")
        elif 'play' in task or 'song' in task:
            song_name = task.replace("play", "").replace("song", "").strip()
            self.play_song(song_name)
        else:
            self.speak("Sorry, I can't perform that task right now.")


# Main program loop
if __name__ == "__main__":
    assistant = VirtualAssistant()

    assistant.speak("Hello, how can I assist you today?")

    while True:
        user_input = assistant.listen()

        if user_input:
            if 'exit' in user_input or 'quit' in user_input:
                assistant.speak("Goodbye!")
                break
            assistant.perform_task(user_input)
