import requests, schedule

def update():
    response = requests.get('http://scrimzone.co/update.php')
    print("Updated")

schedule.every(5).minutes.do(update)