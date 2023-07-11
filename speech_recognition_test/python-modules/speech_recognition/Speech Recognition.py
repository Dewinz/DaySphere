import speech_recognition

with speech_recognition.Microphone() as source:
    print("Speak. Mortal.")
    audio = speech_recognition.Recognizer().listen(source)

try:
    print(speech_recognition.Recognizer().recognize_whisper(audio, language="english"))
except speech_recognition.UnknownValueError:
    print("Audio was not interpretable.")
except speech_recognition.RequestError:
    print("Results could not be requested from Whisper")