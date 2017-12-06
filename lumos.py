#!/usr/bin/env python3.5

import speech_recognition as sr
import requests
import pyaudio
import wave

__author__= "Artur Sak"

'''
Triggers audio file playback when a key phrase is recognized.
@param audio_file - a string containing the name of the .wav file to play
'''
def play_audio(audio_file):
	chunk = 1024
	wf = wave.open(audio_file, 'rb')
	p = pyaudio.PyAudio()

	stream = p.open(
		format = p.get_format_from_width(wf.getsampwidth()),
		channels = wf.getnchannels(),
		rate = wf.getframerate(),
		output = True)
	data = wf.readframes(chunk)
	count = 0

	while len(data) > 0:
		stream.write(data)
		data = wf.readframes(chunk)

	stream.stop_stream()
	stream.close()
	p.terminate()

'''
Activates mic and listens to user commands. Audio is converted to text
via the Google Speech API and if the response matches a key phrase a request
is made to an IFTTT event which turns on room lights
'''
def listen_to_commands():
	r = sr.Recognizer()

	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	try:
		cmd = r.recognize_google(audio)
		cmd = cmd.lower()
		print("You said: " + cmd)
		if cmd == "i love lamp":
			requests.post('https://YOUR_IFFTTT_EVENT_TRIGGER_URL.com')
			play_audio('ilovelamp.wav')
		elif cmd == "lumos" or cmd == "nox":
			requests.post('https://YOUR_IFFTTT_EVENT_TRIGGER_URL.com')
			play_audio('potter.wav')

	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand what you said!")
	except sr.RequestError as e:
		print("Cannot get results from Google Speech Recognition; {0}".format(e))

def main():
	listen_to_commands()

if __name__ == '__main__':
	main()