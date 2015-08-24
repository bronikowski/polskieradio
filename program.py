import requests
import ics
import datetime
from bs4 import BeautifulSoup

PROGRAM_URL = 'http://www.polskieradio.pl/Portal/Schedule/Schedule.aspx'

data = requests.get(PROGRAM_URL)

parsed = BeautifulSoup(data.text, 'html.parser')

boxes = parsed.find_all('div', class_='colBox')

programm = []

PROGRAMMS = ['Jedynka', 'Dwojka', 'Trojka', 'Czworka', 'RadioPoland', 'PR24']

idx = 0

for box in boxes:

    events = []
    today = datetime.datetime.now()
    if box.find('ul', class_='scheduleView'):
        items = box.ul.find_all('li', class_='programmeLi')
        for item in items:
            print('{} — {}'.format(item.find('span', class_='sTime').text, item.find('span', class_='desc').text))
            hour, minutes = item.find('span', class_='sTime').text.split(':')
            begin = datetime.datetime(today.year, today.month, today.day, int(hour), int(minutes))
            events.append(ics.Event(
                name=item.find('span', class_='desc').text,
                begin=begin,
            ))
        calendar = ics.Calendar(events=events)
        with open(PROGRAMMS[idx], 'w') as f:
            f.writelines(calendar)

        idx += 1

