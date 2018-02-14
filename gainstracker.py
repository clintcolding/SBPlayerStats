from urllib import request, parse
from bs4 import BeautifulSoup
import csv
import re

class TeamGains:
    def __init__(self, tid, date, time):
        self.tid = tid
        self.date = date
        self.time = time
        self.contact = 0
        self.power = 0
        self.skill = 0
        self.run = 0
        self.throw = 0
        self.catch = 0
        self.pitch = 0
        self.total = 0

def get_team_gains(training_report):

    # Parse html from uploaded file
    soup = BeautifulSoup(training_report, 'html.parser')
    players = soup.find_all('td', attrs={'align': 'center'})
    full_data = soup.find('table', attrs={'cellpadding': '4'})
    data = full_data.find_all('td')

    # Get team id
    team_row = soup.find('td', attrs={"colspan": "2"})
    tid = team_row.text.strip()
    tid = tid.split('#')
    tid = tid[-1]

    # Get trained datetime
    team_info = full_data.tr.next_sibling.next_sibling
    datetime = team_info.td.next_sibling.next_sibling
    datetime = str(datetime.text.strip())
    datetime = re.split(r'\s{2,}', datetime)
    date = datetime[0]
    time = datetime[1]

    # Get team gains
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]

    contact_gains = 0
    skill_gains = 0
    power_gains = 0
    catch_gains = 0
    throw_gains = 0
    pitch_gains = 0
    run_gains = 0

    for entry in data:
        text = entry.text.strip()
        if "Contact" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            contact_gains += float(''.join(gain))
        if "Skill" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            skill_gains += float(''.join(gain))
        if "Power" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            power_gains += float(''.join(gain))
        if "Catch" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            catch_gains += float(''.join(gain))
        if "Pass" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            throw_gains += float(''.join(gain))
        if "Run" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            run_gains += float(''.join(gain))
        if "Pitch" in text:
            gain = []
            for char in text:
                if char in numbers:
                    gain.append(char)
            pitch_gains += float(''.join(gain))

    total_gains = (contact_gains + skill_gains + power_gains + catch_gains
                   + throw_gains + run_gains + pitch_gains)

    contact_gains = format(contact_gains, '.2f')
    skill_gains = format(skill_gains, '.2f')
    power_gains = format(power_gains, '.2f')
    catch_gains = format(catch_gains, '.2f')
    throw_gains = format(throw_gains, '.2f')
    run_gains = format(run_gains, '.2f')
    pitch_gains = format(pitch_gains, '.2f')
    total_gains = format(total_gains, '.2f')

    myteam = TeamGains(tid, date, time)

    myteam.contact = contact_gains
    myteam.power = power_gains
    myteam.skill = skill_gains
    myteam.run = run_gains
    myteam.throw = throw_gains
    myteam.catch = catch_gains
    myteam.pitch = pitch_gains
    myteam.total = total_gains

    return myteam
