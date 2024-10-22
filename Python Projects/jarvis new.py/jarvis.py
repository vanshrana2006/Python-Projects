import pyttsx3
import sys
from datetime import datetime
import speech_recognition as sr
import os
import subprocess as sp
import requests
import pywhatkit as kit
from email.message import EmailMessage
import smtplib

import os

from dotenv import load_dotenv
import os

load_dotenv()  

USERNAME = os.getenv('USER', 'Vansh')
BOTNAME = os.getenv('BOTNAME', 'Allie')
EMAIL = os.getenv('EMAIL', 'your_email@gmail.com')
PASSWORD = os.getenv('PASSWORD', 'your_password')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key')
OPENWEATHER_APP_ID = os.getenv('OPENWEATHER_APP_ID', 'your_openweather_app_id')
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your_tmdb_api_key')

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190) 
engine.setProperty('volume', 1.0)  

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak(text):
    """Convert text to speech."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred in speak function: {e}")

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}")
    else:
        speak(f"Good Night {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return 'none'
    except sr.RequestError:
        return 'none'

def wait_for_input():
    """Waits for further user input."""
    speak('I am waiting for your command.')
    return take_user_input().lower()

def close_app(app_name):
    """Close the specified application."""
    apps = {
        'notepad': 'notepad++.exe',
        'discord': 'Discord.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe'
    }
    app_exe = apps.get(app_name.lower())
    if app_exe:
        os.system(f'taskkill /im {app_exe} /f')
    else:
        speak(f"Sorry, I don't know how to close {app_name}.")

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'chrome': "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
}

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    os.startfile(paths['notepad'])

def open_discord():
    os.startfile(paths['discord'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])

def open_chrome(url):
    sp.Popen([paths['chrome'], url])


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_google(query):
    url = f"https://www.google.com/search?q={query}"
    open_chrome(url)

def play_on_youtube(video):
    kit.playonyt(video)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_latest_news():
    try:
        news_headlines = []
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general")
        print(res.status_code) 
        print(res.json())  
        if res.status_code == 200:
            articles = res.json()["articles"]
            for article in articles:
                news_headlines.append(article["title"])
            return news_headlines[:5]
        else:
            return ["Unable to fetch news at this time."]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return ["Error occurred while fetching news."]


def get_weather_report(city):
    try:
        res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric")
        print(res.status_code) 
        print(res.json())  
        if res.status_code == 200:
            weather = res.json()["weather"][0]["main"]
            temperature = res.json()["main"]["temp"]
            feels_like = res.json()["main"]["feels_like"]
            return weather, f"{temperature}℃", f"{feels_like}℃"
        else:
            return "Unable to fetch weather report.", "N/A", "N/A"
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Error occurred while fetching weather.", "N/A", "N/A"

def get_trending_movies():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

def get_random_joke():
    headers = {'Accept': 'application/json'}
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if query == 'none':
            speak('Sorry, I didn’t understand that. Could you please repeat?')
            continue  

        if 'bye' in query or 'exit' in query or 'goodbye' in query:
            speak("Goodbye! Have a great day!")
            break

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'google' in query:
            speak('What do you want to search on Google?')
            search_query = wait_for_input()
            if search_query != 'none':
                search_on_google(search_query)
            else:
                speak('Sorry, I didn’t get that. Let’s try again.')

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.')
            print(f'Your IP Address is {ip_address}')

        elif 'youtube' in query:
            speak('What do you want to play on YouTube?')
            video = wait_for_input()
            if video != 'none':
                play_on_youtube(video)
            else:
                speak('Sorry, I didn’t get that. Let’s try again.')

        elif 'search on google' in query:
            speak('What do you want to search on Google?')
            search_query = wait_for_input()
            if search_query != 'none':
                search_on_google(search_query)
            else:
                speak('Sorry, I didn’t get that. Let’s try again.')

        elif "send whatsapp message" in query:
            speak('On what number should I send the message? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message?")
            message = wait_for_input()
            if message != 'none':
                send_whatsapp_message(number, message)
                speak("I've sent the message.")
            else:
                speak('Sorry, I didn’t get the message. Let’s try again.')

        elif "send an email" in query:
            speak("On what email address should I send the message? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject?")
            subject = wait_for_input().capitalize()
            speak("What is the message?")
            message = wait_for_input().capitalize()
            if subject != 'none' and message != 'none':
                if send_email(receiver_address, subject, message):
                    speak("I've sent the email.")
                else:
                    speak("Something went wrong while sending the email. Please check the error logs.")
            else:
                speak('Sorry, I didn’t get the subject or message. Let’s try again.')

        elif 'joke' in query:
            speak("Here's a joke for you:")
            joke = get_random_joke()
            speak(joke)
            print(joke)

        elif "advice" in query:
            speak("Here's an advice for you:")
            advice = get_random_advice()
            speak(advice)
            print(advice)

        elif "trending movies" in query:
            speak("Here are some trending movies:")
            movies = get_trending_movies()
            for movie in movies:
                speak(movie)
                print(movie)
                
        elif "weather" in query:
            speak("Which city do you want the weather report for?")
            city = wait_for_input()
            if city != 'none':
                weather, temperature, feels_like = get_weather_report(city)
                speak(f"The weather in {city} is {weather} with a temperature of {temperature} and it feels like {feels_like}.")
                print(f"The weather in {city} is {weather} with a temperature of {temperature} and it feels like {feels_like}.")
            else:
                speak('Sorry, I didn’t get the city name. Let’s try again.')

        elif 'news' in query:
            speak("Here are the latest headlines:")
            headlines = get_latest_news()
            for headline in headlines:
                speak(headline)
                print(headline)
        else:
            speak("Sorry, I didn't understand that. Could you please repeat?")
