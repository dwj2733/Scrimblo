import discord, asyncio, pickle, time, datetime, os, csv, json, random, chatmodule, requests, secrets, schedule, requests
import pyttsx3
from discord.ext import commands
from discord.utils import get
#from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='!', intents=intents)

players = dict()

def save():
    global players
    json.dump(players,open("players.txt","w+"))

def load():
    global players
    if os.path.exists("players.txt"):
        print("players exists")
        players = json.load(open("players.txt","rb"))
    else:
        print("players.txt does not exist! Does it not exist?")
        players = dict()

def within24h(day):
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    if day in weekdays:
        days = {"monday":"tuesday",
                "tuesday":"wednesday",
                "wednesday":"thursday",
                "thursday":"friday",
                "friday":"saturday",
                "saturday":"sunday",
                "sunday":"monday"}
        today = weekdays[datetime.date.today().weekday()]
        now = datetime.datetime.now()
        if (day == days[today] and now.hour >= 20) or day == today:
            return True
        else:
            return False
    else:
        return False

def getday(delta=0):
    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return weekdays[(datetime.date.today() + datetime.timedelta(days=delta)).weekday()]

def daysuntil(targetday):
    targetday = targetday.lower()
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    dt = 0
    checkday = weekdays[(datetime.date.today() + datetime.timedelta(days=dt)).weekday()]
    while targetday != checkday and dt < 9:
        dt += 1
        checkday = weekdays[(datetime.date.today() + datetime.timedelta(days=dt)).weekday()]
    if dt > 7:
        return -1
    else:
        return dt

def gettomorrow():
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    days = {"monday":"tuesday",
                "tuesday":"wednesday",
                "wednesday":"thursday",
                "thursday":"friday",
                "friday":"saturday",
                "saturday":"sunday",
                "sunday":"monday"}
    return days[weekdays[datetime.date.today().weekday()]]

load()

client = discord.Client(intents=discord.Intents.all())
user = None
@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    ramble_id = 1054874073659879475
    ramble_channel = client.get_channel(ramble_id)
    #await ramble_channel.send("Good morning")
    lastmsg = ""
    signuppost.start()
    while True:
        newmsg = chatmodule.msggen(lastmsg)
        chatlen = random.randint(3,15)
        if random.randint(1,3) == 1:
            lastmsg = ""
            chatlen = 25
        while len(newmsg) < chatlen:
            newmsg = chatmodule.msggen(lastmsg)
        await ramble_channel.send(newmsg)
        lastmsg = newmsg
        await asyncio.sleep(1800)


async def unrole():
    server = client.get_guild(767973379247833099)
    print(server)
    green = discord.utils.get(server.roles, name='Green Team')
    purple = discord.utils.get(server.roles, name='Purple Team')
    pink = discord.utils.get(server.roles, name='Pink Team')
    yellow = discord.utils.get(server.roles, name='Yellow Team')
    beige = discord.utils.get(server.roles, name='Beige Team')
    aqua = discord.utils.get(server.roles, name='Aqua Team')
    magenta = discord.utils.get(server.roles, name='Magenta Team')
    olive = discord.utils.get(server.roles, name='Olive Team')
    spectate = discord.utils.get(server.roles, name='Spectators')
    roles = [green,purple,pink,yellow,aqua,beige,magenta,olive,spectate]
    for a in roles:
        print(a)
        for b in a.members:
            await b.remove_roles(a)
            print(b.id)

#tts = pyttsx3.init()
#tts.setProperty('rate',180)

msgmem = {}
currentcall = False

@client.event
async def on_message(message):
    server = client.get_guild(767973379247833099)
    global msgmem
    #global tts
    global currentcall
    if message.channel in msgmem:
        if not message.content.lower().startswith('&'):
            msgmem[message.channel].append(message.content.lower())
    else:
        msgmem[message.channel] = []
        if not message.content.lower().startswith('&'):
            msgmem[message.channel].append(message.content.lower())


    if len(msgmem[message.channel]) > 10:
        del msgmem[message.channel][0]
    global players
    print("EVENT")
    print(message.content.lower())
    if message.author == client.user:
        return
    if message.content.lower().startswith('&announcerebirth'):
        general_id = 767973462978985995
        message_channel = client.get_channel(general_id)
        #await message_channel.send("I LIVED.")
    #if message.content.lower().startswith('&joinme'):
        #vc = message.author.voice.channel
        #currentcall = await vc.connect()
        #tts.save_to_file("Hello Everybody", 'greeting.mp3')
        #tts.runAndWait()
        #currentcall.play(discord.FFmpegPCMAudio('greeting.mp3'))
    #if message.content.lower().startswith('&say'):
        #if currentcall != False:
            #tts.save_to_file(message.content[4:], 'say.mp3')
            #tts.runAndWait()
            #currentcall.play(discord.FFmpegPCMAudio('say.mp3'))
    #if message.content.lower().startswith('&respond'):
        #if currentcall != False:
            #tts.save_to_file(chatmodule.msggen(message.content.lower() + "\n"), 'resp.mp3')
            #tts.runAndWait()
            #currentcall.play(discord.FFmpegPCMAudio('resp.mp3'))
    if message.content.lower().startswith('&unrole'):
        await unrole()
    if (message.content.lower().find(' blood ')+1) or (message.content.lower().find(' blood.')+1) or (message.content.lower().split()[-1] == "blood"):
        await message.channel.send("Your blood volume is very healthy. The blood volume opposite you is very unhealthy.\nWhy did you abandon your teammates?")
#    if message.content.lower().startswith('&moralleaderboard'):
#        random.seed((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days)
#        name_list = ["Adam", "AJ", "Ali", "An", "Anna", "Azzy", "Ben", "Blake", "Cam", "Casino", "Chimi", "Cece", "Curtis", "Cylako", "Cyrus", "Daev", "Dan", "Danny", "Steve", "Dean", "Diana", "Dominic", "Domonic", "Douglass", "Drago", "Dukky", "Eden", "Erik O.", "Erik Y.", "Ezra", "Garrett", "Garrett H.", "Guld", "Heelie", "Honan", "Hongbaabaa", "J4ke", "Jackson", "Jacob", "Jake", "Jar", "Joel", "Joey", "Jonah", "Kathy", "Leila", "Logan", "Michael", "Mimi", "Noam", "Peter", "Russ", "Sam", "Sam S.", "Sand", "Sean", "Stanley", "Valor", "Will", "Yaveed", "Alana", "Faith", "Evi", "Solari", "Hidiri", "Sarvaris", "Avery", "Gruer"]
#        moralstring = ""
#        moralstring += name_list.pop(name_list.index("Jar")) + " - " + str(random.randint(2000,3700)) + "\n"
#        moralstring += name_list.pop(name_list.index(name_list[random.randint(0,len(name_list)-1)])) + " - " + str(random.randint(100,200)) + "\n"
#        moralstring += name_list.pop(name_list.index(name_list[random.randint(0,len(name_list)-1)])) + " - " + str(random.randint(50,85)) + "\n"
#        moralstring += name_list.pop(name_list.index(name_list[random.randint(0,len(name_list)-1)])) + " - " + str(random.randint(35,40)) + "\n"
#        moralstring += name_list.pop(name_list.index(name_list[random.randint(0,len(name_list)-1)])) + " - " + str(random.randint(30,34)) + "\n"
#        random.seed()
#        await message.channel.send("Top 5 Most Moral Members\nName - Moral Points:\n" + moralstring + "List updates everyday when I consult the universe.")
    if message.content.lower().startswith('&updateroles'):
        if len(message.content.split()) == 1:
            await message.channel.send("Error: Invalid Roles")
            return
        nickname = message.author.nick
        if nickname == None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]
        roles = {'top': 'top', 'jungle': 'jungle', 'mid': 'mid', 'bot': 'bot', 'support': 'support', 'fill': 'fill', 'none': 'null', 'null':'null', 'bottom': 'bot', 'adc': 'bot', 'middle': 'mid', 'jg': 'jungle', 'sup': 'support', 'supp': 'support'}
        role1 = roles.get(message.content.split()[1].lower())
        role2 = 'null'
        role3 = 'null'
        role4 = 'null'
        role5 = 'null'
        if(len(message.content.split()) >= 3):
            role2 = roles.get(message.content.split()[2].lower())
        if(len(message.content.split()) >= 4):
            role3 = roles.get(message.content.split()[3].lower())
        if(len(message.content.split()) >= 5):
            role4 = roles.get(message.content.split()[4].lower())
        if(len(message.content.split()) >= 6):
            role5 = roles.get(message.content.split()[5].lower())
        if(role1 is not None) and (role1 != "null"):
            if(role2 is None):
                role2 = 'null'
            if(role3 is None):
                role3 = 'null'
            if(role4 is None):
                role4 = 'null'
            if(role5 is None):
                role5 = 'null'
            url = 'http://scrimzone.co/players.php'
            myobj = {'updateButton': True,
                    'updatePlayer': nickname,
                    'setLanes': True,
                    'lane1': role1,
                    'lane2': role2,
                    'lane3': role3,
                    'lane4': role4,
                    'lane5': role5}

            x = requests.post(url, data = myobj)

            await message.channel.send("Your roles are now updated to: " + role1 + ", " + role2 + ", " + role3 + ", " + role4 + ", " + role5)
        else:
            await message.channel.send("Error: Invalid Roles")
    if message.content.lower().startswith('&signup'):
        nickname = message.author.nick
        if nickname == None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]

        if len(message.content.split()) == 1:
            await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
        else:
            if message.content.split()[1].lower() == "today":
                signdate = datetime.date.today().strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() == "tomorrow":
                signdate = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                signdate = (datetime.date.today() + datetime.timedelta(days=daysuntil(message.content.split()[1].lower()))).strftime("%Y-%m-%d")
            else:
                await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
                return

            url = 'http://scrimzone.co/signups.php'
            myobj = {'name': nickname, 'date': signdate}

            x = requests.post(url, data = myobj)
            await message.channel.send("Signed up " + nickname + " for " + signdate + ".")
    if message.content.lower().startswith('&unsignup'):
        nickname = message.author.nick
        if nickname == None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]

        if len(message.content.split()) == 1:
            await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
        else:
            if message.content.split()[1].lower() == "today":
                signdate = datetime.date.today().strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() == "tomorrow":
                signdate = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                signdate = (datetime.date.today() + datetime.timedelta(days=daysuntil(message.content.split()[1].lower()))).strftime("%Y-%m-%d")
            else:
                await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
                return

            url = 'http://scrimzone.co/signups.php'
            myobj = {'deleteSignup': 'd3l3t3', 'name': nickname, 'date': signdate}

            x = requests.post(url, data = myobj)
            await message.channel.send("Removed signup of " + nickname + " for " + signdate + ".")

    if message.content.lower().startswith('&welcome') and (message.author in discord.utils.get(server.roles, name='Admins').members):
        if len(message.content.split()) > 1:
            gen_channel = client.get_channel(gen_id)
            welcomeuser = 0
            for w in discord.utils.get(server.roles, name='Registered').members:
                if w.nick == " ".join(message.content.split()[1:]):
                    welcomeuser = w
            if welcomeuser != 0:
                signup_channel = client.get_channel(780732404720467998)
                info_channel = client.get_channel(768195174014124033)
                await gen_channel.send("Welcome " + welcomeuser.mention + "! You have been registered to the website and can now use the " + signup_channel.mention + " and " + info_channel.mention + " channels. Please reach out to any admin (orange names) or DM " + discord.utils.get(server.roles, name='Scrim Bot').members[0].mention + " if you have any questions! Also be sure to familiarize yourself with the ⁠rules and the website: http://scrimzone.co/")
            else:
                await message.channel.send("ERROR: Registered user " + " ".join(message.content.split()[1:]) + " does not exist.")
        else:
            await message.channel.send("ERROR: Command Missing User")
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Thank you, your message has been recieved. We have notified the Admins, and one of them will be in contact with you shortly.")
        adminmsg_id = 1044788321009807421
        message_channel = client.get_channel(adminmsg_id)
        await message_channel.send("_ _\n" + "From: " + message.author.name + "\nMessage Content:\n" + message.content)
    if client.user.mentioned_in(message) and not isinstance(message.channel, discord.DMChannel) and (discord.utils.get(server.roles, name='Scrim Bot').members[0] != message.author):
        await message.channel.send(chatmodule.msggen(message.content.lower() + "\n"),reference=message)
    if not isinstance(message.channel, discord.DMChannel) and (random.randint(1,100) <= 1):
        await message.channel.send(chatmodule.msggen("\n".join(msgmem[message.channel]) + "\n"))
    print(random.randint(1,100))

announce_id = 767973462978985995
cancel_id = 780732404720467998
signup_id = 780732404720467998
gen_id = 770146648177115137
#@tasks.loop(hours=24)
#async def signuppost():
#    today = datetime.date.today()
#    postdate = today + datetime.timedelta(days=0)
#    signup_channel = client.get_channel(signup_id)
#    await signup_channel.send(getday(0) + " " + "(" + postdate.strftime("%m/%d") + "): " + "http://www.scrimzone.co/signups.php?date=" + postdate.strftime("%Y-%m-%d") + "&name=")
#    await unrole()


#@signuppost.before_loop
#async def before():
#    print("Preparing Today's Signup Link Process....")
#    now = datetime.datetime.now()
#    await asyncio.sleep(12)
#    num = 0
#    posttime = 6
#    while (now.hour != posttime) or now.minute > 5:
#        now = datetime.datetime.now()
#        await asyncio.sleep(5)
#        print("waiting",now.hour,now.minute,end="\r")
#        num += 1
#    print("")
#    print("Finished waiting, starting link process...")

client.run(secrets.token)
