from urllib.request import urlopen
from bs4 import BeautifulSoup

class Team:

    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

class Player:

    def __init__(self, Name, Position, Games, AB, Hits,
                 Avg, Singles, Doubles, Triples, HR, RBI, SO, ERA):
        self.Name = Name
        self.Position = Position
        self.Games = Games
        self.AB = AB
        self.Hits = Hits
        self.Avg = Avg
        self.Singles = Singles
        self.Doubles = Doubles
        self.Triples = Triples
        self.HR = HR
        self.RBI = RBI
        self.SO = SO
        self.ERA = ERA

    def get_player_data(self):
        return (self.Name,
                self.Position,
                self.Games,
                self.AB,
                self.Hits,
                self.Avg,
                self.Singles,
                self.Doubles,
                self.Triples,
                self.HR,
                self.RBI,
                self.SO,
                self.ERA)

def get_team_data(tid):

    # Scape and parse the page
    team_page = 'http://smallball.com/go/on.ball.team?tid={0}'.format(tid)
    page = urlopen(team_page)
    soup = BeautifulSoup(page, 'html.parser')

    # Get team name
    team_name = soup.find('td', attrs={'class': 'table_top_name'})
    team_name = team_name.text.strip()

    # Get a list of player names
    team = soup.find('table', attrs={'class': 'table_team_text'})
    data = team.find_all('td', 'table_team_name')
    players = []
    for player in data:
        players.append(player.text.strip())

    # Store data in objects
    myteam = Team(team_name)

    for name in players:
        rawstats = (team.find("td", string=name)).parent
        out = (rawstats.text.strip()).splitlines()

        player = Player(name,
                        out[1],
                        out[2].lstrip(),
                        out[3].lstrip(),
                        out[4].lstrip(),
                        out[5].lstrip(),
                        out[6].lstrip(),
                        out[7].lstrip(),
                        out[8].lstrip(),
                        out[9].lstrip(),
                        out[10].lstrip(),
                        out[11].lstrip(),
                        out[12])

        myteam.add_player(player)

    return myteam
