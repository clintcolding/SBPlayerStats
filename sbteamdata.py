from urllib import request, parse
from bs4 import BeautifulSoup

class Team:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.games = 0
        self.ab = 0
        self.hits = 0
        self.avg = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.hr = 0
        self.rbi = 0
        self.so = 0
        self.era = 0
        self.slg = 0

    def add_player(self, player):
        self.players.append(player)

    def get_team_stats(self):
        active_players = 12
        pitcher_count = 0
        games = 0
        ab = 0
        hits = 0
        singles = 0
        doubles = 0
        triples = 0
        hr = 0
        rbi = 0
        avg = 0
        slg = 0
        so = 0
        era = 0

        for player in self.players:
            if int(player.games) > int(games):
                games = player.games
            if player.games == "0":
                active_players = active_players - 1
            if "-" not in player.era:
                era = era + float(player.era)
                pitcher_count += 1
            ab += int(player.ab)
            hits += int(player.hits)
            singles += int(player.singles)
            doubles += int(player.doubles)
            triples += int(player.triples)
            hr += int(player.hr)
            rbi += int(player.rbi)
            so += int(player.so)
            avg += float(player.avg)
            slg += float(player.slg)

        team_era = era / pitcher_count
        team_era = format(team_era, '.2f')

        team_avg = avg / active_players
        team_avg = format(team_avg, '.3f')
        if team_avg[0] == "0":
            team_avg = team_avg[1:]

        team_slg = slg / active_players
        team_slg = format(team_slg, '.3f')
        if team_slg[0] == "0":
            team_slg = team_slg[1:]

        self.games = games
        self.ab = ab
        self.hits = hits
        self.avg = team_avg
        self.singles = singles
        self.doubles = doubles
        self.triples = triples
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self.era = team_era
        self.slg = team_slg

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

    # Post to SB search page

    search_data = {"oid": tid, "Search": "search"}
    search_url = "http://smallball.com/go/on.ball.team"
    data = parse.urlencode(search_data).encode()
    response = request.urlopen(search_url, data)

    # Parse html from post repsonse
    soup = BeautifulSoup(response, 'html.parser')

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

    myteam.get_team_stats()

    return myteam

def get_pitchers(tid):

    myteam = get_team_data(tid)
    pitchers = []

    for player in myteam.players:
        if "-" not in player.era:
            pitchers.append(player)

    return pitchers
