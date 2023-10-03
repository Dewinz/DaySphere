import speech_recognition as sr
import time
import string
import speechrecognition.commands as commands
import re
from GUI.terminal import TerminalPageFrame

def find_with_spaces(pattern, text):
    pattern = pattern.replace(' ', '')
    pattern_re = re.compile(' *'.join(map(re.escape, pattern)))

    m = pattern_re.search(text)
    if m:
        return m.end()
    
class VR:
    def Record(recognizer, mic):

        if not isinstance(recognizer, sr.Recognizer): raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(mic, sr.Microphone): raise TypeError("`mic` must be `Microphone` instance")

        with mic as source:
            print("Listening...")
            return recognizer.listen(source)
        

    def Recognize(recognizer: sr.Recognizer, audio):
        print("Processing...")
        try:
            text=recognizer.recognize_whisper(audio, "base", False, None, "english", False)
            nopunc = str(text).lower().translate(str.maketrans('', '', string.punctuation))

            for keyword in commands.keywords:
                if keyword in nopunc.replace(" ",""): 
                    print(keyword+" found!")
                    print(commands.runfromstring(nopunc[find_with_spaces(keyword, nopunc)+1:]))
                    break

                else: print(keyword+" not found")

            print(nopunc)
            print("Recognized text: " + text)

        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from the speech recognition service; {0}".format(e))

    def main():
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("Adjusting")
            r.adjust_for_ambient_noise(source, 0.2)

        while True:
            r.listen_in_background(mic, VR.Recognize)
            time.sleep(1000)

if __name__ == "__main__": VR.main()