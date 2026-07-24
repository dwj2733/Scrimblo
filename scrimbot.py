import discord, asyncio, pickle, time, os, csv, json, random, chatmodule, requests, mysecrets, schedule, requests, datetime
from datetime import timedelta
#import pyttsx3
from discord.ext import commands
from discord.utils import get
from zoneinfo import ZoneInfo

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
#bot = commands.Bot(command_prefix='!', intents=intents)
signup_types = ["normal", "late", "tft", "silly"]
last_signups = {signup_type: 0 for signup_type in signup_types}
signup_times = {"normal": "7:55pm Eastern",
                "late": "10:55 Eastern",
                "tft": "8:55 Eastern",
                "silly": "7:55pm Eastern"}
last_day = datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
players = dict()
checked_in = {signup_type: set() for signup_type in signup_types}

def get_eastern_date():
    return datetime.datetime.now(ZoneInfo("America/New_York")).date()

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

def update():
    requests.get('https://scrimzone.co/update.php')
    print("Updated")

async def send_scrimbo_msg(lastmsg):
    server = client.get_guild(767973379247833099)
    newmsg = chatmodule.msggen(lastmsg)
    chatlen = random.randint(3, 15)
    if random.randint(1, 3) == 1:
        lastmsg = ""
        chatlen = 25
        
    while len(newmsg) < chatlen:
        newmsg = chatmodule.msggen(lastmsg)
    words = newmsg.split()
    fixed_words = []

    for word in words:
        if word.startswith(":") and not word.endswith(":"):
            word += ":"
            print('Looking for emoji ' + word.strip(':'))
        if word.startswith(":") and word.endswith(":"):
            emoji = discord.utils.get(server.emojis, name=word.strip(":"))
            print('Looking for emoji ' + word.strip(':'))
            if(emoji):
                word = f"{emoji}"
                containsEmoji = True
        fixed_words.append(word)

    newmsg = " ".join(fixed_words)
    return newmsg

async def ramble_loop():
    await client.wait_until_ready()
    ramble_id = 1054874073659879475
    ramble_channel = client.get_channel(ramble_id)
    lastmsg = ""

    while not client.is_closed():
        newmsg = await send_scrimbo_msg(lastmsg)
        await ramble_channel.send(newmsg)
        lastmsg = newmsg
        await asyncio.sleep(1800)

async def update_loop():
    while True:
        try:
            requests.get('https://scrimzone.co/update.php')
        except Exception as e:
            print("update_loop crashed:", e)
        await asyncio.sleep(300)

async def signup_check_loop():
    await client.wait_until_ready()

    global last_day, last_signups, checked_in

    while not client.is_closed():
        try:
            today = datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
            if today != last_day:
                last_day = today
                last_signups = {signup_type: 0 for signup_type in signup_types}
                checked_in = {signup_type: set() for signup_type in signup_types}

            for event in signup_types:
                url = f"https://scrimzone.co/signuprequests.php?date={today}&type={event}"
                response = requests.get(url).text
                count = int(response.split(",")[0])
                signed_up_players = response.split(",")[1:]

                group_size = 8 if event == "tft" else 10

                num_signup_games = (count // group_size)

                start = (num_signup_games - 1) * group_size
                end = start + group_size

                if num_signup_games >= 1 and num_signup_games > last_signups[event]:
                    channel = client.get_channel(780732404720467998)

                    message_text = ""

                    for i in range(start, end):
                        if i >= len(signed_up_players):
                            break
                        mention = get_user_mention(signed_up_players[i].strip())
                        if mention:
                            message_text += mention + " "

                    message_text += " You are the first " + str(group_size) + " to signup for " + event  + " Scrims today! Please be in lobby at " + signup_times[event]

                    if(event not in ["Silly", "TFT"]):
                        server = client.get_guild(767973379247833099)
                        message_text += ("\n\nPlease keep in mind that signups should be taken seriously as they are crucial for balanced games in the server. " 
                                       "Each game should be played with the intent to win, as such playing while intoxicated is not allowed. "
                                       "If any player on your team is failing to meet these expectations, please let us know via a message to " + discord.utils.get(server.roles, name='Scrim Bot').members[0].mention + ".")

                    await channel.send(message_text)

                    last_signups[event] = num_signup_games
        except Exception as e:
            print("update_loop crashed:", e)
        await asyncio.sleep(1800)

async def unrole_loop():
    await wait_until(3)
    while not client.is_closed():
        await unrole()
        await asyncio.sleep(86400)

async def wait_until(hour: int, minute: int = 0, second: int = 0):
    now = datetime.datetime.now(ZoneInfo("America/New_York"))
    target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)

    # If target time already passed today, schedule for tomorrow
    if target <= now:
        target += timedelta(days=1)

    # Seconds until target time
    wait_seconds = (target - now).total_seconds()
    await asyncio.sleep(wait_seconds)

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
        today = weekdays[get_eastern_date().weekday()]
        now = datetime.datetime.now(ZoneInfo("America/New_York"))
        if (day == days[today] and now.hour >= 20) or day == today:
            return True
        else:
            return False
    else:
        return False

def getday(delta=0):
    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return weekdays[(get_eastern_date() + datetime.timedelta(days=delta)).weekday()]

def daysuntil(targetday):
    targetday = targetday.lower()
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    dt = 0
    checkday = weekdays[(get_eastern_date() + datetime.timedelta(days=dt)).weekday()]
    while targetday != checkday and dt < 9:
        dt += 1
        checkday = weekdays[(get_eastern_date() + datetime.timedelta(days=dt)).weekday()]
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
    return days[weekdays[get_eastern_date().weekday()]]

load()

client = discord.Client(intents=discord.Intents.all())
user = None
@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    asyncio.create_task(ramble_loop())
    asyncio.create_task(update_loop())
    asyncio.create_task(signup_check_loop())
    asyncio.create_task(unrole_loop())


async def format_signuplist(signdate, signtype, guild):
    url = f"https://scrimzone.co/signuprequests.php?date={signdate}&type={signtype}"
    response = requests.get(url).text
    parts = response.split(",")
    players_raw = [p.strip() for p in parts[1:] if p.strip()]

    in_lobby = get_lobby_members(guild)

    ready = [p for p in players_raw if p in checked_in[signtype] or p in in_lobby]
    missing = [p for p in players_raw if p not in checked_in[signtype] and p not in in_lobby]

    output = parts[0]
    if ready:
        output += "\nReady: " + ", ".join(ready)
    if missing:
        output += "\nMissing: " + ", ".join(missing)

    return output

def get_lobby_members(guild):
    lobby_channel = guild.get_channel(768004380729278474)
    in_lobby = set()
    if lobby_channel:
        for member in lobby_channel.members:
            nick = member.nick or member.global_name
            if nick and nick.find("(") != -1:
                nick = nick[nick.find("(") + 1:nick.find(")")]
            if nick:
                in_lobby.add(nick)
    return in_lobby

async def unrole():
    global checked_in
    checked_in = {signup_type: set() for signup_type in signup_types}

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
        if a is None:
            continue
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
    global checked_in
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
    words = message.content.lower().replace(".", "").replace(",", "").split()

    if "blood" in words:
        await message.channel.send(
            "Your blood volume is very healthy. The blood volume opposite you is very unhealthy.\n"
            "Why did you abandon your teammates?"
        )
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
            url = 'https://scrimzone.co/players.php'
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
    if message.content.lower().startswith('&signup') and not message.content.lower().startswith('&signuplist'):
        nickname = message.author.nick
        if nickname == None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]

        if len(message.content.split()) == 1:
            await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
        else:
            if message.content.split()[1].lower() == "today":
                signdate = get_eastern_date().strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() == "tomorrow":
                signdate = (get_eastern_date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                signdate = (get_eastern_date() + datetime.timedelta(days=daysuntil(message.content.split()[1].lower()))).strftime("%Y-%m-%d")
            else:
                await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
                return
            if len(message.content.split()) > 2:
                signtype = message.content.split()[2].lower()
                if signtype in signup_types:
                    url = 'https://scrimzone.co/signuprequests.php'
                    myobj = {'name': nickname, 'date': signdate, 'type': signtype}

                    x = requests.post(url, data = myobj)
                    await message.channel.send("Signed up " + nickname + " for " + signtype + " signups for " + signdate + ".")
                    return 
                else:
                    await message.channel.send("ERROR: Invalid Type. Please enter one of the following: " + ', '.join(signup_types) + ".")
                    return      

            url = 'https://scrimzone.co/signuprequests.php'
            myobj = {'name': nickname, 'date': signdate}

            x = requests.post(url, data = myobj)
            await message.channel.send("Signed up " + nickname + " for " + signdate + ".")

    if message.content.lower().startswith('&signuplate'):
        await message.channel.send("You typed `&signuplate`. Did you mean `&signup [day] late`?")
        return

    if message.content.lower().startswith('&signuplist'):
        parts = message.content.split()
        if len(parts) == 1:
            signdate = get_eastern_date().strftime("%Y-%m-%d")
            signtype = "normal"
            show_missing = False
        else:
            if parts[1].lower() == "today":
                signdate = get_eastern_date().strftime("%Y-%m-%d")
            elif parts[1].lower() == "tomorrow":
                signdate = (get_eastern_date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif parts[1].lower() in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                signdate = (get_eastern_date() + datetime.timedelta(days=daysuntil(parts[1].lower()))).strftime("%Y-%m-%d")
            else:
                await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
                return

            signtype = "normal"
            show_missing = False

            if len(parts) > 2:
                if parts[2].lower() in signup_types:
                    signtype = parts[2].lower()
                elif parts[2].lower() == "missing":
                    show_missing = True
                else:
                    await message.channel.send("ERROR: Invalid type. Please enter one of the following: " + ', '.join(signup_types) + ".")
                    return

            if len(parts) > 3:
                if parts[3].lower() == "missing":
                    show_missing = True

        if show_missing:
            output = await format_signuplist(signdate, signtype, server)
        else:
            url = 'https://scrimzone.co/signuprequests.php'
            myobj = {'date': signdate, 'type': signtype}
            x = requests.post(url, data=myobj)
            output = x.text

    await message.channel.send(output)
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
                signdate = get_eastern_date().strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() == "tomorrow":
                signdate = (get_eastern_date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            elif message.content.split()[1].lower() in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                signdate = (get_eastern_date() + datetime.timedelta(days=daysuntil(message.content.split()[1].lower()))).strftime("%Y-%m-%d")
            else:
                await message.channel.send("ERROR: Invalid day. Please enter today/tomorrow or weekday name.")
                return
            if len(message.content.split()) > 2:
                signtype = message.content.split()[2].lower()
                if signtype in signup_types:
                    url = 'https://scrimzone.co/signuprequests.php'
                    myobj = {'deleteSignup': 'd3l3t3', 'name': nickname, 'date': signdate, 'type': signtype}

                    x = requests.post(url, data = myobj)
                    await message.channel.send("Removed " + signtype + " signup of " + nickname + " for " + signdate + ".")
                    return 
                else:
                    await message.channel.send("ERROR: Invalid Type. Please enter one of the following: " + ', '.join(signup_types) + ".")
                    return     

            url = 'https://scrimzone.co/signuprequests.php'
            myobj = {'deleteSignup': 'd3l3t3', 'name': nickname, 'date': signdate}

            x = requests.post(url, data = myobj)
            await message.channel.send("Removed signup of " + nickname + " for " + signdate + ".")



    if message.content.lower().startswith('&welcome') and (message.author in discord.utils.get(server.roles, name='Admins').members):
        if len(message.content.split()) > 1:
            gen_channel = client.get_channel(gen_id)
            welcomemention = get_user_mention(" ".join(message.content.split()[1:]))
            if welcomemention != 0:
                signup_channel = client.get_channel(780732404720467998)
                info_channel = client.get_channel(768195174014124033)
                await gen_channel.send("Welcome " + welcomemention + "! You have been registered to the website and can now use the " + signup_channel.mention + " and " + info_channel.mention + " channels. Please reach out to any admin (orange names) or DM " + discord.utils.get(server.roles, name='Scrim Bot').members[0].mention + " if you have any questions! Also be sure to familiarize yourself with the ⁠rules and the website: https://scrimzone.co/")
            else:
                await message.channel.send("ERROR: Registered user " + " ".join(message.content.split()[1:]) + " does not exist.")
        else:
            await message.channel.send("ERROR: Command Missing User")

    if message.content.lower().startswith('&spectate'):
      server = client.get_guild(767973379247833099)
    
      # Get the Spectators role
      spectator_role = discord.utils.get(server.roles, name='Spectators')
    
      if spectator_role is None:
        await message.channel.send("Error: Spectators role not found.")
        return

      # Add role to user
      await message.author.add_roles(spectator_role)
      await message.channel.send(f"{message.author.mention} is now a spectator.")

    if message.content.lower().startswith('&checkin'):
        parts = message.content.split()
        nickname = message.author.nick
        if nickname is None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]

        signdate = get_eastern_date().strftime("%Y-%m-%d")

        if len(parts) > 1:
            signtype = parts[1].lower()
            if signtype not in signup_types:
                await message.channel.send("ERROR: Invalid type. Please enter one of the following: " + ', '.join(signup_types) + ".")
                return
            url = f"https://scrimzone.co/signuprequests.php?date={signdate}&type={signtype}"
            response = requests.get(url).text
            signed_up_players = [p.strip() for p in response.split(",")[1:]]
            if nickname in signed_up_players:
                checked_in[signtype].add(nickname)
                await message.channel.send(f"{nickname} has been checked in for {signtype}!")
            else:
                await message.channel.send(f"{nickname} is not signed up for {signtype} today.")
        else:
            found_types = []
            for signtype in signup_types:
                url = f"https://scrimzone.co/signuprequests.php?date={signdate}&type={signtype}"
                response = requests.get(url).text
                signed_up_players = [p.strip() for p in response.split(",")[1:]]
                if nickname in signed_up_players:
                    found_types.append(signtype)
                    checked_in[signtype].add(nickname)

            if found_types:
                await message.channel.send(f"{nickname} has been checked in for {', '.join(found_types)}!")
            else:
                await message.channel.send(f"{nickname} is not signed up for today.")

    if message.content.lower().startswith('&checkout'):
        nickname = message.author.nick
        if nickname is None:
            nickname = message.author.global_name
        if nickname.find("(") != -1:
            nickname = nickname[nickname.find("(") + 1:nickname.find(")")]

        removed = False
        for signtype in signup_types:
            if nickname in checked_in[signtype]:
                checked_in[signtype].discard(nickname)
                removed = True
                await message.channel.send(f"{nickname} has been checked out of {signtype}.")
                break

        if not removed:
            await message.channel.send(f"{nickname} is not currently checked in.")

    if message.content.lower().startswith('&pingmissing'):
        admin_role = discord.utils.get(server.roles, id=793182421470281791)
        if message.author not in admin_role.members:
            return

        if len(message.content.split()) > 1:
            signtype = message.content.split()[1].lower()
            if signtype not in signup_types:
                await message.channel.send("ERROR: Invalid type. Please enter one of the following: " + ', '.join(signup_types) + ".")
                return
        else:
            signtype = "normal"

        signdate = get_eastern_date().strftime("%Y-%m-%d")
        url = f"https://scrimzone.co/signuprequests.php?date={signdate}&type={signtype}"
        response = requests.get(url).text
        parts = response.split(",")
        players_raw = [p.strip() for p in parts[1:] if p.strip()]

        in_lobby = get_lobby_members(server)

        group_size = 8 if signtype == "tft" else 10
        num_full_groups = len(players_raw) // group_size
        players_in_scope = players_raw[:num_full_groups * group_size]

        missing = [p for p in players_in_scope if p not in checked_in[signtype] and p not in in_lobby]

        signup_channel = client.get_channel(780732404720467998)
        if not missing:
            await signup_channel.send("Everyone in the current groups is present!")
            return

        mentions = [get_user_mention(p) for p in missing]
        await signup_channel.send("The following players are not yet present: " + " ".join(mentions))

    if message.content.lower().startswith('&unspectate'):
      server = client.get_guild(767973379247833099)
    
      # Get the Spectators role
      spectator_role = discord.utils.get(server.roles, name='Spectators')
    
      if spectator_role is None:
        await message.channel.send("Error: Spectators role not found.")
        return

      if message.author.voice:
        await message.author.move_to(None)

      # Remove role from user
      await message.author.remove_roles(spectator_role)
      await message.channel.send(f"{message.author.mention} is no longer a spectator.")
    
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Thank you, your message has been recieved. We have notified the Admins, and one of them will be in contact with you shortly.")
        adminmsg_id = 1044788321009807421
        message_channel = client.get_channel(adminmsg_id)
        await message_channel.send("_ _\n" + "From: " + message.author.name + "\nMessage Content:\n" + message.content)
    if client.user.mentioned_in(message) and not isinstance(message.channel, discord.DMChannel) and (discord.utils.get(server.roles, name='Scrim Bot').members[0] != message.author):
        msgtxt = await send_scrimbo_msg(message.content.lower() + "\n")
        await message.channel.send(msgtxt,reference=message)
    if not isinstance(message.channel, discord.DMChannel) and (random.randint(1,100) <= 1):
        msgtxt = await send_scrimbo_msg("\n".join(msgmem[message.channel]) + "\n")
        await message.channel.send(msgtxt)
    print(random.randint(1,100))

def get_user_mention(name):
    server = client.get_guild(767973379247833099)
    for w in discord.utils.get(server.roles, name='Registered').members:
        if w.nick == name:
            return w.mention
    return name



announce_id = 767973462978985995
cancel_id = 780732404720467998
signup_id = 780732404720467998
gen_id = 770146648177115137
#@tasks.loop(hours=24)
#async def signuppost():
#    today = datetime.date.today()
#    postdate = today + datetime.timedelta(days=0)
#    signup_channel = client.get_channel(signup_id)
#    await signup_channel.send(getday(0) + " " + "(" + postdate.strftime("%m/%d") + "): " + "https://www.scrimzone.co/signups.php?date=" + postdate.strftime("%Y-%m-%d") + "&name=")
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

client.run(mysecrets.token)
