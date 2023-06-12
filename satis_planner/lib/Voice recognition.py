import speech_recognition as sr
import time

def callback(recognizer, audio):
        print("callback")
        try:
            text=recognizer.recognize_whisper(audio, "base", False, None, "english", False)
            if "key word" in recognizer.recognize_whisper(audio, "base", False, None, "english", False): print("Keyword") 
            else: print("No keyword")
            print("Recognized text: " + text)
            time.sleep(20)
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
            time.sleep(20)
        except sr.RequestError as e:
            print("Could not request results from the speech recognition service; {0}".format(e))
            time.sleep(20)

def startListening():
    r = sr.Recognizer()
    source = sr.Microphone()
    print("Listening...")
    audio = r.listen_in_background(source, callback)
    time.sleep(200)