import string
import br
lena={}
keywords=["DaySphere",
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
          "dayscaler"
          ]

activation={
    "add": br.activation.add,
    "what is": br.activation.add
}

for it in activation.keys():
    lena[len(it)]=it

for i in range(len(keywords)):
    keywords[i]=keywords[i].lower().translate(str.maketrans('', '', string.punctuation)).replace(" ","")