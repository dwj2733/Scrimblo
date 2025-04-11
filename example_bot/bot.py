import nextcord
import schedule
import time
import requests
from nextcord.ext import commands

TESTING_GUILD_ID = 1360080396087328951  # Replace with your guild ID

bot = commands.Bot()


def update():
	response = requests.get('http://scrimzone.co/update.php')

schedule.every(5).minutes.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)

bot.run('MTM2MDA3Nzk0MjI5Nzg1NDIxNQ.GrsXkw.mOMqqTqNaaghkFrYWMGwSskF5I5YWY75Ojq_ZI')

