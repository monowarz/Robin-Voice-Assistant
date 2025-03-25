import speech_recognition as sr
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib.request as urllib2
import json
import os
import sys
import re
import wikipedia
import random
import webbrowser
import smtplib
import requests
import subprocess
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from time import strftime
import datetime


class RobinAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.weather_api_key = "*****************"
        self.news_url = "https://news.google.com/news/rss"
        self.wallpaper_api_key = "***************"

    def speak(self, text):
        """Outputs the given text as speech."""
        print(text)
        os.system("say " + text)

    def listen(self):
        """Listens for user commands and returns the recognized text."""
        with sr.Microphone() as source:
            print("Say something...")
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("....")
            return self.listen()

    def open_reddit(self, command):
        """Opens Reddit based on user request."""
        reg_ex = re.search(r'open reddit (.*)', command)
        url = "https://www.reddit.com/"
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + "r/" + subreddit
        webbrowser.open(url)
        self.speak("The Reddit content has been opened for you Sir.")

    def open_website(self, command):
        """Opens a website requested by the user."""
        reg_ex = re.search(r'open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = f"https://www.{domain}"
            webbrowser.open(url)
            self.speak("The website you requested has been opened.")

    def greet(self):
        """Greets the user based on the time of day."""
        day_time = int(strftime("%H"))
        if day_time < 12:
            self.speak("Hello Sir. Good morning.")
        elif 12 <= day_time < 18:
            self.speak("Hello Sir. Good afternoon.")
        else:
            self.speak("Hello Sir. Good evening.")

    def fetch_weather(self, command):
        """Fetches the current weather for a specified city."""
        reg_ex = re.search("current weather in (.*)", command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key=self.weather_api_key)
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit="celsius")
            self.speak(
                f"Current weather in {city} is {k}. The maximum temperature is {x['temp_max']:.2f} and the minimum temperature is {x['temp_min']:.2f} degrees Celsius."
            )

    def tell_time(self):
        """Tells the current time."""
        now = datetime.datetime.now()
        self.speak(f"Current time is {now.hour} hours {now.minute} minutes.")

    def fetch_news(self):
        """Fetches top news headlines."""
        try:
            client = urlopen(self.news_url)
            xml_page = client.read()
            client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:15]:
                self.speak(news.title.text)
        except Exception as e:
            print(e)

    def send_email(self):
        """Sends an email to a specified recipient."""
        self.speak("Who is the recipient?")
        recipient = self.listen()
        if "david" in recipient:
            self.speak("What should I say to him?")
            content = self.listen()
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("your_email@gmail.com", "your_password")
            mail.sendmail("your_email@gmail.com", "recipient_email@gmail.com", content)
            mail.close()
            self.speak("Email has been sent successfully.")
        else:
            self.speak("I don't know what you mean!")

    def launch_application(self, command):
        """Launches an application."""
        reg_ex = re.search("launch (.*)", command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + ".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            self.speak("Launched!")

    def play_song(self):
        """Plays a requested song from YouTube."""
        self.speak("What song shall I play Sir?")
        mysong = self.listen()
        if mysong:
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(" ", "+")
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html, "lxml")
            url_list = [
                "https://www.youtube.com" + vid["href"]
                for vid in soup1.findAll(attrs={"class": "yt-uix-tile-link"})
                if ("https://www.youtube.com" + vid["href"]).startswith("https://www.youtube.com/watch?v=")
            ]
            if url_list:
                final_url = url_list[0]
                ydl_opts = {}
                os.chdir("/Users/NAME_HERE/Documents/videos/")
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([final_url])
                vlc.play("/Users/NAME_HERE/Documents/videos/")
            else:
                self.speak("I couldn't find anything on YouTube.")

    def change_wallpaper(self):
        """Changes the desktop wallpaper using an image from Unsplash."""
        url = f"https://api.unsplash.com/photos/random?client_id={self.wallpaper_api_key}"
        response = urllib2.urlopen(url)
        json_data = json.loads(response.read())
        photo_url = json_data["urls"]["full"]
        wallpaper_path = "/Users/USER_NAME_HERE/Documents/wallpaper/a"
        urllib.urlretrieve(photo_url, wallpaper_path)
        subprocess.call(["killall Dock"], shell=True)
        self.speak("Wallpaper changed successfully.")

    def search_wikipedia(self, command):
        """Fetches Wikipedia information based on user query."""
        reg_ex = re.search("tell me about (.*)", command)
        if reg_ex:
            topic = reg_ex.group(1)
            try:
                summary = wikipedia.summary(topic, sentences=2)
                self.speak(summary)
            except wikipedia.exceptions.DisambiguationError:
                self.speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                self.speak("Sorry, I couldn't find information on that.")

    def execute_command(self, command):
        """Executes a user command."""
        if "open reddit" in command:
            self.open_reddit(command)
        elif "shutdown" in command:
            self.speak("Bye bye Sir. Have a nice day")
            sys.exit()
        elif "open" in command:
            self.open_website(command)
        elif "hello" in command:
            self.greet()
        elif "current weather" in command:
            self.fetch_weather(command)
        elif "time" in command:
            self.tell_time()
        elif "news for today" in command:
            self.fetch_news()
        elif "email" in command:
            self.send_email()
        elif "launch" in command:
            self.launch_application(command)
        elif "play me a song" in command:
            self.play_song()
        elif "change wallpaper" in command:
            self.change_wallpaper()
        elif "tell me about" in command:
            self.search_wikipedia(command)

    def start(self):
        """Starts the assistant."""
        self.speak("Hello, I am Robin, your assistant. How can I help you?")
        while True:
            command = self.listen()
            self.execute_command(command)


# Initialize and start Robin Assistant
assistant = RobinAssistant()
assistant.start()
