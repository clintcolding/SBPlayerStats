from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sbteamdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    name = db.Column(db.String)
    stars = db.Column(db.Integer)
    stadium = db.Column(db.String)
    pl = db.Column(db.String)
    pl_position = db.Column(db.String)
    trained = db.Column(db.String)
    games = db.Column(db.Integer)
    ab = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    avg = db.Column(db.String)
    singles = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)
    slg = db.Column(db.String)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    pct = db.Column(db.String)
    rs = db.Column(db.Integer)
    ra = db.Column(db.Integer)

    def __init__(self, time, season, teamid, name, stars, stadium, pl, pl_position,
                 trained, games, ab, hits, avg, singles, doubles, triples,
                 hr, rbi, so, era, slg, wins, losses, pct, rs, ra):
        self.time = time
        self.season = season
        self.teamid = teamid
        self.name = name
        self.stars = stars
        self.stadium = stadium
        self.pl = pl
        self.pl_position = pl_position
        self.trained = trained
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
        self.wins = wins
        self.losses = losses
        self.pct = pct
        self.rs = rs
        self.ra = ra

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    name = db.Column(db.String)
    position = db.Column(db.String)
    games = db.Column(db.Integer)
    ab = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    avg = db.Column(db.String)
    singles = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)
    slg = db.Column(db.String)

    def __init__(self, season, teamid, playerid, name, position, games, ab, hits,
                 avg, singles, doubles, triples, hr, rbi, so, era, slg):
        self.season = season
        self.teamid = teamid
        self.playerid = playerid
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

class Pitcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    teamid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    name = db.Column(db.String)
    games = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)

    def __init__(self, season, teamid, playerid, name, games, so, era):
        self.season = season
        self.teamid = teamid
        self.playerid = playerid
        self.name = name
        self.games = games
        self.so = so
        self.era = era


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tid = request.form['teamid']

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>', methods=['GET', 'POST'])
def stats(tid):
    current_season = sbteamdata.get_current_season()
    seasons = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
    team = Team.query.filter_by(teamid=tid, season=current_season).first()

    if team and (team.time - datetime.now()).total_seconds() > -600:
        players = Player.query.filter_by(teamid=tid, season=current_season).all()
        pitchers = Pitcher.query.filter_by(teamid=tid, season=current_season).all()
        updated = team.time.strftime('Updated on %B %d at %I:%M %p')

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

        team = Team.query.filter_by(teamid=tid, season=current_season).first()
        players = Player.query.filter_by(teamid=tid, season=current_season).all()
        pitchers = Pitcher.query.filter_by(teamid=tid, season=current_season).all()
        updated = team.time.strftime('Updated on %B %d at %I:%M %p')

    return render_template('stats.html', updated=updated, seasons=seasons, team=team, players=players, pitchers=pitchers)

@app.route('/refreshstats', methods=['POST'])
def refresh_stats():
    tid = request.form['tid']

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

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>/<season>')
def seasonstats(tid, season):
    current_season = sbteamdata.get_current_season()

    if season != 'all' and int(current_season) == int(season):

        return redirect('/stats/{0}'.format(tid))
    
    else:
        if season == "all":
            team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
            players = Player.query.filter_by(teamid=tid).all()
            pitchers = Pitcher.query.filter_by(teamid=tid).all()
            stats = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).first()

            return render_template('allstats.html', team=team, stats=stats, players=players, pitchers=pitchers)
        
        else:
            team = Team.query.filter_by(teamid=tid).order_by(Team.season.desc()).all()
            players = Player.query.filter_by(teamid=tid, season=season).all()
            pitchers = Pitcher.query.filter_by(teamid=tid, season=season).all()

            for entry in team:
                if entry.season == int(season):
                    stats = entry

            return render_template('seasonstats.html', team=team, stats=stats, players=players, pitchers=pitchers)

@app.route('/leaders')
def leaders():
    current_season = sbteamdata.get_current_season()

    teams = Team.query.filter_by(season=current_season).filter(Team.games >= 5)
    players = Player.query.filter_by(season=current_season).filter(Player.games >= 5)
    pitchers = Pitcher.query.filter_by(season=current_season).filter(Pitcher.games >= 5)

    return render_template('leaders.html', teams=teams, players=players, pitchers=pitchers)

@app.route('/gameleaders')
def gameleaders():
    current_season = sbteamdata.get_current_season()

    teams = Team.query.filter_by(season=current_season).filter(Team.games >= 5)
    players = Player.query.filter_by(season=current_season).filter(Player.games >= 5)
    pitchers = Pitcher.query.filter_by(season=current_season).filter(Pitcher.games >= 5)

    return render_template('gameleaders.html', teams=teams, players=players, pitchers=pitchers)

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
