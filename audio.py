from tkinter import *
import speech_recognition as sr 


class Guardador:
		
	def transcripcion(self):

		r = sr.Recognizer()

		with sr.Microphone() as source:
			print("Speak: ")
			audio = r.listen(source)

		try:
			x= r.recognize_google(audio, language='es-ES')
			#print("transcription: " + x)
			entrada.insert(0, x + ' ')
		except sr.UnknownValueError:
			print("Audio unintelligible")
		except sr.RequestError as e:
			print("Cannot obtain results; {0}".format(e))

