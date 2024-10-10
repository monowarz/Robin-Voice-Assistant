# Robin - Personal Voice Assistant
![image](https://github.com/monowarz/Robin-Voice-Assistant/blob/master/Python%20Voice%20Assistant.png)

# Robin - Personal Voice Assistant

Robin is a Python-based voice assistant that helps automate everyday tasks. With voice commands, you can browse the web, send emails, get weather updates, play songs, and much more. 

## Features

- **Open websites**: Open Reddit subreddits, or any website just by saying its name.
- **Send emails**: Compose and send emails through voice prompts.
- **Weather updates**: Get current weather conditions for any city.
- **Play music**: Play a song using VLC media player.
- **News**: Get the top stories of the day from Google News.
- **Change wallpaper**: Automatically change your desktop wallpaper with images from Unsplash.
- **Tell a joke**: Hear random dad jokes for a quick laugh.
- **Time updates**: Ask for the current time.
- **Search Wikipedia**: Get summaries on topics directly from Wikipedia.

## Requirements

To run Robin, you need the following Python packages:

```bash
pip install speechrecognition
pip install pyowm
pip install wikipedia
pip install youtube_dl
pip install vlc
pip install bs4
```

You’ll also need these dependencies:
- [VLC media player](https://www.videolan.org/vlc/) for playing media files.
- A microphone and speakers to interact with the assistant.

## Setup and Usage

1. Clone this repository:

```bash
git clone https://github.com/yourusername/robin-voice-assistant.git
cd robin-voice-assistant
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the assistant:

```bash
python robin.py
```

4. Speak commands like:
   - **"Open reddit"** to browse Reddit.
   - **"Send email"** to compose an email.
   - **"What's the weather in [city]"** for weather updates.
   - **"Play me a song"** to play music through VLC.

5. To see available commands, say **"Help me"**.

## Commands

- **Open a subreddit**: `Open Reddit [subreddit name]`
- **Visit a website**: `Open [website name]`
- **Send an email**: `Email [recipient name]`
- **Tell me a joke**: `Tell a joke`
- **Weather update**: `Current weather in [city]`
- **Check the time**: `Time`
- **Change wallpaper**: `Change wallpaper`
- **Play a song**: `Play me a song`
- **Today's news**: `News for today`
- **Learn about something**: `Tell me about [topic]`

## Contributions

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions, improvements, or bug fixes.

Enjoy automating your tasks with Robin!
