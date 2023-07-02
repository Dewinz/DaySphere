import speech_recognition as sr
import time
r = sr.Recognizer()
while(True):
    with sr.Microphone() as source:
        print("Adjusting")
        r.adjust_for_ambient_noise(source, 0.2)
        print("Listening...")
        audio = r.listen(source)
    print("Processing...")
    try:
        text=r.recognize_whisper(audio, "base", False, None, "english", False)
        if "key word" in r.recognize_whisper(audio, "base", False, None, "english", False): print("Keyword") 
        else: print("No keyword")
        print("Recognized text: " + text)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from the speech recognition service; {0}".format(e))