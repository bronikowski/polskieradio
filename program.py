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

    today = datetime.datetime.now()
    if box.find('ul', class_='scheduleView'):
        items = box.ul.find_all('li', class_='programmeLi')
        events = []
        for item in items:
            hour, minutes = item.find('span', class_='sTime').text.split(':')
            begin = datetime.datetime(today.year, today.month, today.day, int(hour), int(minutes))
            end = None
            if events:
                # did we put anything before on the events stack>
                events[-1].end = begin 
            events.append(ics.Event(
                name=item.find('span', class_='desc').text,
                begin=begin,
                end=end,
            ))
        calendar = ics.Calendar(events=events)

        ics_file = '{}.ics'.format(PROGRAMMS[idx])

        with open(ics_file, 'w') as f:
            f.writelines(calendar)
            print('Wrote {} to disk'.format(ics_file))
        idx += 1

