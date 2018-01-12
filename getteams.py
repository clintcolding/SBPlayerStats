from urllib import request, parse
from bs4 import BeautifulSoup
from app import db, Team, Player, Pitcher
from flask_sqlalchemy import SQLAlchemy
import sbteamdata

league = 1

if league == 1:
    teams = 10
if league == 2:
    teams = 25

# Scape and parse the page
league_page = 'http://www.smallball.com/ball/leagues/pro{0}.shtml'.format(league)
page = request.urlopen(league_page)
soup = BeautifulSoup(page, 'html.parser')

team_table = soup.find('table', attrs={'class': 'table_team_text'})
data = team_table.find_all('td', 'table_team_numbers')

rows = []
for entry in data:
    rows.append(entry.text.strip())

index_counter = 2

teamids = []
for i in range(teams):
    tid = rows[index_counter:(index_counter+1)]
    tid = str(tid)[2:]
    tid = tid[:-2]
    teamids.append(tid)

    index_counter = index_counter + 8

for tid in teamids:
    stats = sbteamdata.get_team_data(tid)
    pitchers = sbteamdata.get_pitchers(tid)

    team = Team.query.filter_by(teamid=tid).first()
    players = Player.query.filter_by(teamid=tid).all()
    p_players = Pitcher.query.filter_by(teamid=tid).all()

    if team:
        db.session.delete(team)
        db.session.commit()

    new_entry = Team(tid, stats.name, stats.games, stats.ab, stats.hits, stats.avg, stats.singles,
        stats.doubles, stats.triples, stats.hr, stats.rbi, stats.so, stats.era, stats.slg, stats.wins,
        stats.losses, stats.pct, stats.rs, stats.ra)
    db.session.add(new_entry)

    if players:
        for player in players:
            db.session.delete(player)
            db.session.commit()

    for player in stats.players:
        new_entry = Player(tid, player.id, player.name, player.position, player.games, player.ab, 
            player.hits, player.avg, player.singles, player.doubles, player.triples, player.hr, player.rbi, 
            player.so, player.era, player.slg)
        db.session.add(new_entry)

    if p_players:
        for player in p_players:
            db.session.delete(player)
            db.session.commit()
    for player in pitchers:
        if player.era != "-":
            new_entry = Pitcher(tid, player.id, player.name, player.games, player.so, player.era)
            db.session.add(new_entry)
    db.session.commit()