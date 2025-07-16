import random, sys, re, datetime
Memory = 16
def memweight(occur):
    if occur < 1:
        occur = 1
    return 2*(2**(-1*abs(occur-2)))
MemMultOrAdd = "Mult"
brain = {}
#thanks https://stackoverflow.com/questions/26778073/python-read-char-in-text-until-whitespace
#and https://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
def generator(path):
    wordI = ''
    with open(path, "r",encoding="UTF-8") as file:
        while True:
            char = file.read(1)
            if char == "?":
                char = " "
            if char == "\n":
                char = " N "
            if char == " ":
                if wordI:
                    yield wordI
                    wordI = ''
            elif char == '':
                if wordI:
                    yield wordI
                break
            else:
                if char == " N ":
                    wordI += char
                else:
                    wordI += char.lower()

#data = data.replace("\n"," N ")
outtype = "Words"
WORDS = []
NEWW = []
wordcount = 0
loadtype = "s"#input("(F)ast High Mem Load, (M)edium Low Memory load, or (S)low Low Memory Load?").lower()
if loadtype == "f":
    text_file = open("chinese.txt", "r",encoding="UTF-8")
    a = datetime.datetime.now()
    DATA = text_file.read().lower().replace("\n"," N ")
    WORDS = list(DATA)
    for s in WORDS:
        if [s] != re.findall(r"[\w]+|[^\s\w]", s):
            SPLIT = re.findall(r"[\w]+|[^\s\w]", s)
            for t in SPLIT:
                if t != SPLIT[0]:
                    NEWW.append("S" + t)
                else:
                    NEWW.append(t)
        else:
            NEWW.append(s)
    for v in range(len(NEWW)):
        if NEWW[v] == "SN":
            NEWW[v] = "S\n"
        if NEWW[v] == "N":
            NEWW[v] = "\n"
    wordcount = len(NEWW)
    for x in range(len(NEWW)-1):
        word = NEWW[x]
        nextword = NEWW[x+1]
        if word not in brain:
            brain[word] = {}
        if nextword not in brain[word]:
            brain[word][nextword] = 1
        else:
            brain[word][nextword] += 1
    text_file.close()
elif loadtype == "s":
    text_file = generator("scrim.txt")#input("File Path?"))
    #if "?" in text_file:
    #    text_file.remove("?")
    a = datetime.datetime.now()
    for u in text_file:
        if [u] != re.findall(r"[\w]+|[^\s\w]", u):
            SPLIT = re.findall(r"[\w]+|[^\s\w]", u)
            for t in SPLIT:
                if t != SPLIT[0]:
                    NEWW.append("S" + t)
                else:
                    NEWW.append(t)
        else:
            NEWW.append(u)
        for v in range(len(NEWW)):
            if NEWW[v] == "SN":
                NEWW[v] = "S\n"
            if NEWW[v] == "N":
                NEWW[v] = "\n"
        wordcount += len(NEWW) - 1
        for x in range(len(NEWW)-1):
            word = NEWW[x]
            nextword = NEWW[x+1]
            if word not in brain:
                brain[word] = {}
            if nextword not in brain[word]:
                brain[word][nextword] = 1
            else:
                brain[word][nextword] += 1
        NEWW = [NEWW[-1]]
    text_file.close()
else:
    text_file = open(input("File Path?"), "r",encoding="UTF-8")
    a = datetime.datetime.now()
    u = text_file.readline().lower().replace("\n"," N ")
    while u:
        u = u.split(" ")
        for r in u:
            if [r] != re.findall(r"[\w]+|[^\s\w]", r):
                SPLIT = re.findall(r"[\w]+|[^\s\w]", r)
                for t in SPLIT:
                    if t != SPLIT[0]:
                        NEWW.append("S" + t)
                    else:
                        NEWW.append(t)
            else:
                NEWW.append(r)
        for v in range(len(NEWW)):
            if NEWW[v] == "SN":
                NEWW[v] = "S\n"
            if NEWW[v] == "N":
                NEWW[v] = "\n"
        wordcount += len(NEWW) - 1
        for x in range(len(NEWW)-1):
            word = NEWW[x]
            nextword = NEWW[x+1]
            if word not in brain:
                brain[word] = {}
            if nextword not in brain[word]:
                brain[word][nextword] = 1
            else:
                brain[word][nextword] += 1
        NEWW = [NEWW[-1]]
        u = text_file.readline().lower().replace("\n"," N ")
    text_file.close()
b = datetime.datetime.now()
print("Loading Time:",b-a)
print("Words: ",wordcount)
print("Unique Words: ",len(brain))
#print(data[:25]+"...")
#print(str(list(brain.items())[:8])[:64])
print("Brain Size:",sys.getsizeof(brain))
#GENERATE

def msggen(msg):
    if "?" in brain:
        brain.pop("?")
    output = []
    #msg += " S\n"
    msg = msg.replace("\n"," ")
    msgF = msg.replace('!', '').replace('.', '').replace(')', '').lower().split()
    if len(msgF) > 0:
        output += msgF[:-1]
        startw = msgF[-1]
    else:
        startw = ""
    if startw == "":
        retword = "\n"
        while retword == "\n" or retword == "NULL":
            retword = random.choice(list(brain))
        output.append(retword)
    else:
        output.append(startw)
    iters = 100#int(input("Sequence Length?")) - 1
    WORDMEM = []
    for h in msgF:
        if h in brain:
            WORDMEM.append(h)
    for y in range(iters):
        curword = output[-1]
        #print(output)
        #print(curword)
        if curword in brain:
            wordchoices = list(brain[curword])
            wordweights = []
            for z in wordchoices:
                wordweights.append(brain[curword][z])
            #special weight changes
            for q in range(len(wordweights)):
                if "?" in wordchoices[q]:
                    wordweights[q] = wordweights[q] + 10000
                #wordweights[q] = wordweights[q]/(len(wordchoices[q])**3)
            #square = prioritize higher probability
            pass
            #memory auditing
            for q in range(len(wordweights)):
                try:
                    wordweights[q] = wordweights[q] * memweight(WORDMEM.count(wordchoices[q]))
                except IndexError:
                    wordweights[q] = 0.00000001
            chosenword = random.choices(wordchoices, weights=wordweights, k=1)
            output.append(chosenword[0])
            WORDMEM.append(chosenword[0])
        else:
            output.append(random.choice(list(brain)))
            WORDMEM.append(output[-1])
        if len(WORDMEM) > 64:
            while len(WORDMEM) > 64:
                WORDMEM.pop(0)
    if "P" == "P":
        if outtype == "Char":
            outtxt = "".join(output).replace("\n ","\n").replace("pedophile","[REDACTED]").replace("pedo","[REDACTED]")
        else:
            outtxt = " ".join(output).replace("\n ","\n").replace(" S","").replace("\nS","\n").replace("|","\n").replace("pedophile","[REDACTED]").replace("pedo","[REDACTED]")
    else:
        pass
    #print(outtxt)
    outtxt = outtxt.replace("@","")
    outtxt = outtxt[outtxt.find("\n") + 1:]
    outtxt = outtxt[outtxt.find(" ") + 1:]
    if outtxt[0:2] == "? ":
        outtxt = outtxt[outtxt.find("? ") + 1:]
    while outtxt[0] == " ":
        outtxt = outtxt[outtxt.find(" ") + 1:]
    outtxt = outtxt[0:outtxt.find("\n")]
    while ": " in outtxt:
        outtxt = outtxt[outtxt.find(": ") + 2:]
    return outtxt

def brainsearch(keyw):
    for key, value in brain.items():
        if key == keyw:
            print(key + ": " + str(brain[key]))
    print("")
    print("Searching in Values...")
    print("")
    sortdict = {}
    for key, value in brain.items():
        if keyw in value:
            #print(key + ": " + str(brain[key]))
            sortdict[key] = brain[key][keyw]
    dict(sorted(sortdict.items(), key=lambda item: item[1]))
    for key, value in sortdict.items():
        print(key,"-",value)

"""
print("DEBUG:")
def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

for name, size in sorted(((name, sys.getsizeof(value)) for name, value in locals().items()),
                         key= lambda x: -x[1])[:10]:
    print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))
"""
