from urllib import request, parse
from bs4 import BeautifulSoup
from app import app, db, Team, Player, Pitcher
from flask_sqlalchemy import SQLAlchemy
import sbteamdata
from datetime import datetime

league = 2

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

with app.app_context():

    for tid in teamids:
        current_season = sbteamdata.get_current_season()
        team = Team.query.filter_by(teamid=tid, season=current_season).first()

        if team and (team.time - datetime.now()).total_seconds() > -600:
            players = Player.query.filter_by(teamid=tid, season=current_season).all()
            pitchers = Pitcher.query.filter_by(teamid=tid, season=current_season).all()
        
        else:
            stats = sbteamdata.get_team_data(tid)

            team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
            players = Player.query.filter_by(teamid=tid, season=stats.season).all()
            pitchers = Pitcher.query.filter_by(teamid=tid, season=stats.season).all()

            for entry in team:
                if entry.season == int(stats.season):
                    db.session.delete(entry)
                    db.session.commit()

            new_entry = Team(datetime.now(), stats.season, tid, stats.name, stats.stars, stats.stadium,
                            stats.pl, stats.pl_position, stats.trained, stats.games, stats.ab, stats.hits,
                            stats.avg, stats.singles, stats.doubles, stats.triples, stats.hr,
                            stats.rbi, stats.so, stats.era, stats.slg, stats.wins, stats.losses,
                            stats.pct, stats.rs, stats.ra)
            db.session.add(new_entry)

            if players:
                for player in players:
                    db.session.delete(player)
                    db.session.commit()

            for player in stats.players:
                new_entry = Player(stats.season, tid, player.id, player.name, player.position, player.games,
                                player.ab, player.hits, player.avg, player.singles, player.doubles,
                                player.triples, player.hr, player.rbi, player.so, player.era, player.slg)
                db.session.add(new_entry)

            if pitchers:
                for player in pitchers:
                    db.session.delete(player)
                    db.session.commit()
            for player in stats.pitchers:
                new_entry = Pitcher(stats.season, tid, player.id, player.name, player.games,
                                    player.so, player.era)
                db.session.add(new_entry)
            db.session.commit()