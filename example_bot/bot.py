import nextcord
import schedule
import time
from nextcord.ext import commands

TESTING_GUILD_ID = 1360080396087328951  # Replace with your guild ID

bot = commands.Bot()

'''async def open_website():
	try:
		await webbrowser.open_new_tab("http://www.scrimzone.co/update.php")
	except:
		print("CAM HAPPY")
	print("CAMS TEARS TT")
'''
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello!")


async def job():
	channel = client.get_channel(1360099712199295028)
	await channel.send('pRiNT pRIntS tO tErMInAl')

await job()

#schedule.every(10).minutes.do(job)
#schedule.every(25).seconds.do(open_website)
#chedule.every(1).seconds.do(job)

print("pRiNT pRIntS tO tErMInAl")

while True:
    schedule.run_pending()
    time.sleep(1)


bot.run('MTM2MDA3Nzk0MjI5Nzg1NDIxNQ.GrsXkw.mOMqqTqNaaghkFrYWMGwSskF5I5YWY75Ojq_ZI')

