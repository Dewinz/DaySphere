from string import punctuation
from json import load
from re import Match, search

function_dictionary = {}

for key, value in load(open("functions.json")).items():
    try: function_dictionary[len(key)][key] = value
    except:
        function_dictionary[len(key)] = {}
        function_dictionary[len(key)][key] = value


keywords=[
    # Added new keywords.
    "thanks for here",
    "thanks for",
    "base here",
    "base fare",
    "thanks sir",
    "they sphere",
    "theysphere",
    "basesphere",
    "base fair",
    "basesphere",
    "ay super",
    "daysville",
    "day 2",
    "desu",
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
    keywords[i]=keywords[i].lower().translate(str.maketrans('', '', punctuation)).replace(" ","")


class activation:
    def add(string):
        ret=0
        if string[:1] == " ": string = string[1:]
        while string!="":
            try: n1=int(search(r'\d*', string).group())
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
    global function_dictionary
    for lenak in function_dictionary.keys():
        try: function = function_dictionary[lenak][inputstr[:lenak].lower()]
        except: continue
        
        if type(function) == str: function = [function, "str"]

        if function[1] == "str":
            return eval(function[0] + f"(\"{inputstr[lenak:].lower()}\")")
        elif function[1] == "var":
            return eval(function[0] + f"(*{tuple(inputstr[lenak:].lower().split(' ')[1:])})")
        else:
            return eval(function[0] + f"(*{tuple(inputstr[lenak:].lower().split(' ')[1:function[1]+1])})")