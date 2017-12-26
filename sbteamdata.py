from urllib.request import urlopen
from bs4 import BeautifulSoup

class Team:

    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

class Player:

    def __init__(self, id, name, position, games, ab, hits,
                 avg, singles, doubles, triples, hr, rbi, so, era, slg=0):
        self.id = id
        self.name = name
        self.position = position
        self.games = games
        self.ab = ab
        self.hits = hits
        self.avg = avg
        self.singles = singles
        self.doubles = doubles
        self.triples = triples
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self.era = era
        self.slg = slg

    def __str__(self):
        return str(self.id + " " +
                   self.name + " " +
                   self.position + " " +
                   self.games + " " +
                   self.ab + " " +
                   self.hits + " " +
                   self.avg + " " +
                   self.singles + " " +
                   self.doubles + " " +
                   self.triples + " " +
                   self.hr + " " +
                   self.rbi + " " +
                   self.so + " " +
                   self.era + " " +
                   self.slg)

    def __getitem__(self, name):
        return str(self.name,
                   self.position,
                   self.games,
                   self.ab,
                   self.hits,
                   self.avg,
                   self.singles,
                   self.doubles,
                   self.triples,
                   self.hr,
                   self.rbi,
                   self.so,
                   self.era,
                   self.slg)

    def compute_slg(self):

        totalbases = int(self.singles) + (int(self.doubles)*2) + (int(self.triples)*3) + (int(self.hr)*4)

        if self.ab == "0":
            slg = 0
        else:
            slg = (totalbases / int(self.ab))
            slg = format(slg, '.3f')
            if slg[0] == "0":
                slg = slg[1:]
        return str(slg)

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
    id = 1

    for name in players:
        rawstats = (team.find("td", string=name)).parent
        out = (rawstats.text.strip()).splitlines()

        player = Player(str(id),
                        name,
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

        player.slg = player.compute_slg()

        myteam.add_player(player)

        id += 1

    return myteam

def get_team_stats(tid):

    myteam = get_team_data(tid)

    teamstats = []

    for entry in myteam.players:
        teamstats.append(str(entry))

    return teamstats

def get_player_stats(tid):

    myteam = get_team_data(tid)

    for player in myteam.players:
        return player.name, player.position

def get_pitchers(tid):

    myteam = get_team_data(tid)
    pitchers = []

    for player in myteam.players:
        if player.era is not "-":
            pitchers.append(player)

    return pitchers