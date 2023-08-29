import re
class activation:
    def add(string):
        ret=0
        while string!="":
            try: n1=int(re.search(r'\d+', string).group())
            except: break
            ret+=n1
            string=string[len(str(n1)):]
            if string[:4] == " and": string=string[5:]
            elif string[:5] == " plus": string=string[6:]
            elif string[:2] == " +": string=string[3:]
            elif string[:1] == " ": string=string[1:]
            else: break
        print(ret)
        return ret