from urllib import request, parse
from bs4 import BeautifulSoup
import inflection

class Team:

    def __init__(self, name):
        self.name = name
        self.tid = 0
        self.season = 0
        self.stars = 0
        self.stadium = "Intel"
        self.pl = 0
        self.pl_position = 0
        self.trained = 0
        self.wins = 0
        self.losses = 0
        self.pct = 0
        self.rs = 0
        self.ra = 0
        self.players = []
        self.pitchers = []
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

        if int(pitcher_count) == 0:
            team_era = "0"
        else:
            team_era = era / pitcher_count
            team_era = format(team_era, '.2f')

        if int(active_players) == 0:
            team_avg = ".000"
            team_slg = "0"
        else:
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

    def get_team_pitchers(self):

        for player in self.players:
            if "-" not in player.era:
                self.pitchers.append(player)
            elif player.so is not "0":
                self.pitchers.append(player)

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

    # Request sb home page
    search_url = "http://www.smallball.com/ball/home/index.shtml"
    response = request.urlopen(search_url)

    # Parse html from repsonse
    soup = BeautifulSoup(response, 'html.parser')
    season = soup.find('td', attrs={'class': 'text_22'})
    season = season.text.strip()
    season = season[7:]

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

    # Get team id
    team_id = soup.find('td', attrs={'class': 'table_top_id'})
    team_id = team_id.text.strip()
    team_id = team_id[5:]

    # Get team star level and last trained

    team_star = soup.find('td', attrs={'class': 'table_top_2'})
    team_star_level = team_star.find('img')['src']
    team_star_level = team_star_level[18:]
    team_star_level = team_star_level[:-4]
    team_last_trained = (team_star.text.strip()).title()

    # Get team PL and PL position

    leagues = soup.find_all('td', attrs={'class': 'table_team_bottom1'})
    league = leagues[3]
    league = league.find('a')
    league = league.get('href')
    league = str(league).replace("/ball/leagues/pro","")
    pl = str(league).replace(".shtml","")

    position = soup.find_all('td', attrs={'class': 'table_team_bottom2'})
    position = position[3].text.strip()
    if position != "n/a":
        pl_position = inflection.ordinalize(position)
    else:
        pl_position = "n/a"

    # Get home stadium

    stadium_id = soup.find('img', attrs={'border': '2'})

    if "None" in str(stadium_id):
        stadium = "park2"
    if "park4" in str(stadium_id):
        stadium = "park4"
    if "park5" in str(stadium_id):
        stadium = "park5"
    if "park6" in str(stadium_id):
        stadium = "park6"
    if "park7" in str(stadium_id):
        stadium = "park7"
    if "park8" in str(stadium_id):
        stadium = "park8"
    if "park9" in str(stadium_id):
        stadium = "park9"
    if "park10" in str(stadium_id):
        stadium = "park10"
    if "park11" in str(stadium_id):
        stadium = "park11"
    if "park12" in str(stadium_id):
        stadium = "park12"
    if "park13" in str(stadium_id):
        stadium = "park13"

    # Get wins/losses and runs scored/against
    game_data = soup.find_all('td', attrs={'class': 'recent_text_right'})

    game_score = []
    game_result = []
    count = 0
    game_wins = 0
    game_losses = 0
    game_runs_for = 0
    game_runs_against = 0

    for entry in game_data:
        if 'width="10%"' in str(entry) and '?' not in str(entry):
            game_result.append(entry.text.strip())
        if 'width="13%"' in str(entry) and 'n/a' not in str(entry):
            game_score.append(entry.text.strip())

    for i in game_result:
        score_split = game_score[count].split(":")
        if i == "W":
            game_wins += 1
            if int(score_split[0]) > int(score_split[1]):
                game_runs_for += int(score_split[0])
                game_runs_against += int(score_split[1])
            else:
                game_runs_for += int(score_split[1])
                game_runs_against += int(score_split[0])
        if i == "L":
            game_losses += 1
            if int(score_split[0]) < int(score_split[1]):
                game_runs_for += int(score_split[0])
                game_runs_against += int(score_split[1])
            else:
                game_runs_for += int(score_split[1])
                game_runs_against += int(score_split[0])
        count += 1

    # Calculate pct

    if int(game_wins) == 0:
        game_pct = "0"
    else:
        game_pct = int(game_wins) / (int(game_wins) + int(game_losses))
        game_pct = format(game_pct, '.3f')

        if game_pct[0] == "0":
            game_pct = game_pct[1:]

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
    myteam.get_team_pitchers()
    myteam.tid = team_id
    myteam.season = season
    myteam.stars = int(team_star_level)
    myteam.trained = team_last_trained
    myteam.pl = pl
    myteam.pl_position = pl_position
    myteam.stadium = stadium
    myteam.wins = game_wins
    myteam.losses = game_losses
    myteam.pct = game_pct
    myteam.rs = game_runs_for
    myteam.ra = game_runs_against

    return myteam

def get_current_season():
    # Request sb home page
    search_url = "http://www.smallball.com/ball/home/index.shtml"
    response = request.urlopen(search_url)

    # Parse html from repsonse
    soup = BeautifulSoup(response, 'html.parser')
    season = soup.find('td', attrs={'class': 'text_22'})
    season = season.text.strip()
    season = season[7:]

    return season