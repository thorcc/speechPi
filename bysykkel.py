import requests

# Speech to text
import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
sr.Microphone.list_microphone_names()

# Text to speech
from gtts import gTTS
from io import BytesIO

# For playing mp3 through the terminal
import os

# For string-matching
from fuzzywuzzy import fuzz

def vis_alle_holdeplasser():
 holdeplasser = []
 raw_response = requests.get('https://oslobysykkel.no/api/v1/stations', headers={'Client-Identifier': '15111a56c5b41b49f82d98a9595be3c3'})
 response = raw_response.json()
 for station in response["stations"]:
    holdeplasser.append(station["title"])
 return holdeplasser

def holdeplass_id(navn):
 raw_response = requests.get('https://oslobysykkel.no/api/v1/stations', headers={'Client-Identifier': '15111a56c5b41b49f82d98a9595be3c3'})
 response = raw_response.json()
 for station in response["stations"]:
    if(station["title"]==navn):
        return station["id"]

def antall_ledig_sykler(stopp):
 id = holdeplass_id(stopp)
 raw_response = requests.get('https://oslobysykkel.no/api/v1/stations/availability/', headers={'Client-Identifier': '15111a56c5b41b49f82d98a9595be3c3'})
 response = raw_response.json()
 #print(response)
 for station in response["stations"]:
    if(station["id"]==id):
        return station["availability"]["bikes"]

def tipp_holdeplass(tale):
    high_score = 0
    beste_holdeplass = ""
    for holdeplass in vis_alle_holdeplasser():
        score = fuzz.ratio(holdeplass, tale)
        if score > high_score:
            high_score = score
            beste_holdeplass = holdeplass
    return beste_holdeplass, score

def speech_to_string():
    print("Mic start")
    print("Snakk nå")
    with mic as source:
        audio = r.listen(source)
    print("Mic done")
    return r.recognize_google(audio, language='no')

def string_to_bikestop(string):
    holdeplass = tipp_holdeplass(string)
    print("Jeg er " + str(holdeplass[1]) + "% sikker på at du mener ", holdeplass[0])
    return holdeplass[0]

def bikestop_to_printText(bikestop):
    free_bikes = antall_ledig_sykler(bikestop)
    if free_bikes == 0:
        free_bikes = "ingen"
    return str(free_bikes) + " ledige sykler i " + bikestop

def string_to_mp3_save(string,filename):
    # String to mp3
    mp3_fp = BytesIO()
    tts = gTTS(string, 'no')
    tts.save(filename)

def play_mp3_mac(filename):
    file = filename
    os.system("afplay " + file)

def play_mp3_linux(filename):
    # apt install mpg123
    file = filename
    os.system("mpg123 " + file)

def program():
    tale = speech_to_string()
    stopp = string_to_bikestop(tale)
    tekst = bikestop_to_printText(stopp)
    filnavn = "bysykkel.mp3"
    string_to_mp3_save(tekst,filnavn)
    play_mp3_mac(filnavn)

program()