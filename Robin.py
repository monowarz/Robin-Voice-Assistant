import speech_recognition as sr
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib2
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
from urllib2 import urlopen
from time import strftime


def robinreply(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def usercom():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = usercom();
    return command

def robin_start(command):
    "if statements for executing commands"

    #open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        robinreply('The Reddit content has been opened for you Sir.')

    elif 'shutdown' in command:
        robinreply('Bye bye Sir. Have a nice day')
        sys.exit()

    #open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            robinreply('The website you have requested has been opened for you Sir.')
        else:
            pass

    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            robinreply('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            robinreply('Hello Sir. Good afternoon')
        else:
            robinreply('Hello Sir. Good evening')

    elif 'help me' in command:
        robinreply("""
        Here’s what I can help you with:

        1. Browse a Reddit subreddit: Simply name the subreddit, and I’ll open it in your browser.
        2. Visit a website (e.g., open xyz.com): Replace 'xyz' with the site you want to visit.
        3. Send an email: I’ll ask for the recipient and message details step-by-step.
        4. Want a joke? Say "Tell a joke" or "another joke," and I’ll give you a dad joke.
        5. Get the weather forecast in {city name}: I’ll update you with the current weather and temperature for your city.
        6. Say hello, and I’ll greet you depending on the time of day.
        7. Play a song: I can play your requested video or song on VLC.
        8. Update your wallpaper: Let me change your desktop wallpaper for you.
        9. Today’s news: I’ll read out the latest headlines.
        10. Check the time: I’ll tell you the current time from your system.
        11. Top Google news stories: I’ll bring you the latest top stories from Google News.
        12. Learn about something: Ask me to tell you about any topic, and I’ll provide details.

        """)

    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='*****************')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            robinreply('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        robinreply('Current time is %d hours %d minutes' % (now.hour, now.minute))

    elif 'news for today' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                robinreply(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)

    elif 'email' in command:
        robinreply('Who is the recipient?')
        recipient = usercom()
        if 'david' in recipient:
            robinreply('What should I say to him?')
            content = usercom()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('nageshsinghc@gmail.com', '*************')
            mail.sendmail('nageshsingh4@gmail.com', 'amdp.hauhan@gmail.com', content)
            mail.close()
            robinreply('Email has been sent successfuly. You can check your inbox.')
        else:
            robinreply('I don\'t know what you mean!')

    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)

        robinreply('Launched!')

    elif 'play me a song' in command:
        path = '/Users/NAME_HERE/Documents/videos/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        robinreply('What song shall I play Sir?')
        mysong = usercom()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []


            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)


            url = url_list[0]
            ydl_opts = {}


            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)

            if flag == 0:
                robinreply('I have not found anything in Youtube ')

    elif 'change wallpaper' in command:
        folder = '/Users/USER_NAME_HERE/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        api_key = '***************'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key 
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo, "/Users/USER_NAME_HERE/Documents/wallpaper/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        robinreply('wallpaper changed successfully')

    #ask me anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                robinreply(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                robinreply(e)

robinreply('Hi User, I am Robin and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')

while True:
    robin_start(usercom())
