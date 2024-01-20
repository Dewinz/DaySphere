from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError
from string import punctuation
import speechrecognition.commands as commands
from GUI.terminal import feedback, history
from re import compile, escape

listening = False

def find_with_spaces(pattern: str, text: str):
    pattern = pattern.replace(' ', '')
    pattern_re = compile(' *'.join(map(escape, pattern)))

    m = pattern_re.search(text)
    if m:
        return m.end()
    
class VR:
    recog = Recognizer()
    mic = Microphone()
    recog.dynamic_energy_threshold = False

    def Record(recognizer, mic):

        if not isinstance(recognizer, Recognizer): raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(mic, Microphone): raise TypeError("`mic` must be `Microphone` instance")

        with mic as source:
            print("Listening...")
            return recognizer.listen(source)
        

    def Recognize(recognizer: Recognizer, audio):
        history("Processing...")
        try:
            text=recognizer.recognize_whisper(audio, "small.en", False, None, "english", False)
            nopunc = str(text).lower().translate(str.maketrans('', '', punctuation))

            for keyword in commands.keywords:
                if keyword in nopunc.replace(" ",""): 
                    print(keyword+" found!")
                    # TODO Change to more readable text.
                    feedback(terminal_command=nopunc[find_with_spaces(keyword, nopunc)+1:], voice=True)
                    break

                 # else: print(keyword+" not found")

            history(nopunc)
             # print("Recognized text: " + text)

        except UnknownValueError:
            print("Speech recognition could not understand audio")
        except RequestError as e:
            print("Could not request results from the speech recognition service; {0}".format(e))

    def main():
        global listening_thread, listening

        if not listening: 
            with VR.mic as source:
                history("Adjusting")
                VR.recog.adjust_for_ambient_noise(source, 0.5)
                print(VR.recog.energy_threshold)
            
            listening_thread = VR.recog.listen_in_background(VR.mic, VR.Recognize)
            history("Listening...")
        else: listening_thread()
        listening = not listening

if __name__ == "__main__": VR.main()