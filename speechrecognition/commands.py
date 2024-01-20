from string import punctuation
from json import load
from re import Match, search, sub
from communication.client import save_data, request_data
from datetime import datetime

function_dictionary = {}

for key, value in load(open("functions.json")).items():
    try: function_dictionary[len(key)][key] = value
    except:
        function_dictionary[len(key)] = {}
        function_dictionary[len(key)][key] = value


keywords=[
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
    "deysphere",
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
    "date fair",
    "day steer",
    "daysear",
    "day share",
    "taste air",
    "daysayer"
    ]

for i in range(len(keywords)):
    keywords[i]=keywords[i].lower().translate(str.maketrans('', '', punctuation)).replace(" ","")


class activation:
    def add(string):
        ret=0
        if string[:1] == " ": string = string[1:]
        while string!="":
            try: n1=int(search(r'[0-9]*', string).group())
            except: break
            ret+=n1
            string=string[len(str(n1)):]
            if string[:4] == " and": string=string[5:]
            elif string[:5] == " plus": string=string[6:]
            elif string[:2] == " +": string=string[3:]
            elif string[:1] == " ": string=string[1:]
            else: break
        return ret
    
    def schedule(string):
        def save_event(event, day, month=datetime.now().month, year=datetime.now().year):
            print(f"{day}/{month}/{year}")
            data = request_data("Calendar")
            try: 
                if len(data[f"{day}/{month}/{year}"]) < 26:
                    data[f"{day}/{month}/{year}"].append(event)
                    save_data(data, "Calendar")
            except:
                data[f"{day}/{month}/{year}"] = [event]
                save_data(data, "Calendar")
        
        string = sub(r'for the |4 the |on the |for ', "", string, 1)
        if string[:8] == "tomorrow": return save_event(string[9:], datetime.now().day+1)
        if search(r'[0-9]*', string) == None or "": return "Could not find a day"
        day = search(r'[0-9]*', string).group()
        print(day)
        string = string[len(day)+3:]
        try: 
            month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"].index(search(r'\w* \w*', string).group().lower().split(" ")[1])+1
            print(month)
            print(string+"STRPS")
            string = sub(r'\w* \w* ', "", string, 1)
            print(string + "YAHA!")
            if search(r'^20\d{2} ', string) != None:
                save_event(string[5:], day, month, string[:4])
            else:
                print("HUZZAH!")
                save_event(string, day, month)
        except: 
            save_event(string, day)


def runfromstring(inputstr:str):
    global function_dictionary
    for lenak in function_dictionary.keys():
        try: function = function_dictionary[lenak][inputstr[:lenak].lower()]
        except: continue
        
        if type(function) == str: function = [function, "str"]

        if function[1] == "str":
            return eval(function[0] + f"(\"{inputstr[lenak+1:].lower()}\")")
        elif function[1] == "var":
            return eval(function[0] + f"(*{tuple(inputstr[lenak+1:].lower().split(' ')[1:])})")
        else:
            return eval(function[0] + f"(*{tuple(inputstr[lenak+1:].lower().split(' ')[1:function[1]+1])})")