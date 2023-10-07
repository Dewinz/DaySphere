import string
import json
import re


megadic = {}

for key, value in json.load(open("functions.json")).items():
    try: megadic[len(key)][key] = value
    except:
        megadic[len(key)] = {}
        megadic[len(key)][key] = value



keywords=[
    # Added new keywords.
    "Thanks for here"
    "Thanks for",
    "Base here",
    "Base fare",
    "Thanks sir",
    "they sphere",
    "theysphere",
    "basesphere",
    # Till here.
    "DaySphere",
    "Day's fair",
    "Day's here",
    "Days failed",
    "Days, Firdies",
    "Days, Fierce",
    "day's fear",
    "어케desfere",
    "days fare",
    "day is fair",
    "days for you",
    "days for",
    "d-sphere",
    "de-sphere",
    "dayscare",
    "daysfailer",
    "dayscaler",
    "date fair"
    ]

for i in range(len(keywords)):
    keywords[i]=keywords[i].lower().translate(str.maketrans('', '', string.punctuation)).replace(" ","")



class activation:
    def add(string):
        ret=0
        if string[:1] == " ": string = string[1:]
        while string!="":
            try: n1=int(re.search(r'\d*', string).group())
            except: break
            ret+=n1
            string=string[len(str(n1)):]
            if string[:4] == " and": string=string[5:]
            elif string[:5] == " plus": string=string[6:]
            elif string[:2] == " +": string=string[3:]
            elif string[:1] == " ": string=string[1:]
            else: break
        return ret
    


def runfromstring(inputstr):
    global megadic
    for lenak in megadic.keys():
        try: return eval(megadic[lenak][inputstr[:lenak]]+f"(\"{inputstr[lenak:]}\")")
        except: continue
    
