import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "55c1a0869c5847169b964b7094c1a623"

def speak(text):
    engine.say(text)
    engine.runAndWait()

# def speak(text):
#     tts = gTTS(text)
#     tts.save("temp.mp3")

#     pygame.mixer.init()
#     pygame.mixer.music.load("temp.mp3")
#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     pygame.mixer.music.unload()
#     os.remove("temp.mp3")  # Clean up the temporary file

def aiProcess(command):
    client = OpenAI(
        api_key="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",
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")

    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")

    elif "open masoom sharma song" in c.lower():
        webbrowser.open("https://youtu.be/j67MMW8h9Ic?si=Wx_NeVugeEB_JzNm")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])


    else:
        output = aiProcess(c)
        speak(output)
        


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Yes Boss")
                with sr.Microphone() as source:
                    print("Jarvis is listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
            
        