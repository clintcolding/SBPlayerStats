from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sbteamdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Recent(db.Model):
    teamid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)

    def __init__(self, teamid, time):
        self.teamid = teamid
        self.time = time

class Team(db.Model):
    teamid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
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

    def __init__(self, teamid, name, games, ab, hits, avg, 
                 singles, doubles, triples, hr, rbi, so, era, slg,
                 wins, losses, pct, rs, ra):
        self.teamid = teamid
        self.name = name
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

    def __init__(self, teamid, playerid, name, position, games, ab, hits,
                 avg, singles, doubles, triples, hr, rbi, so, era, slg):
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
    teamid = db.Column(db.Integer)
    playerid = db.Column(db.Integer)
    name = db.Column(db.String)
    games = db.Column(db.Integer)
    so = db.Column(db.Integer)
    era = db.Column(db.String)

    def __init__(self, teamid, playerid, name, games, so, era):
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
    
    team = Recent.query.filter_by(teamid=tid).first()

    if team:
        team.time = datetime.now()
    else:
        new_entry = Recent(tid, datetime.now())
        db.session.add(new_entry)
    db.session.commit()

    return redirect('/stats/{0}'.format(tid))

@app.route('/stats/<tid>', methods=['GET', 'POST'])
def stats(tid):
    stats = sbteamdata.get_team_data(tid)

    team = Team.query.filter_by(teamid=tid).first()
    players = Player.query.filter_by(teamid=tid).all()
    pitchers = Pitcher.query.filter_by(teamid=tid).all()

    if team:
        db.session.delete(team)
        db.session.commit()

    if stats.games != 0:
        new_entry = Team(tid, stats.name, stats.games, stats.ab, stats.hits, stats.avg, stats.singles,
            stats.doubles, stats.triples, stats.hr, stats.rbi, stats.so, stats.era, stats.slg, stats.wins,
            stats.losses, stats.pct, stats.rs, stats.ra)
        db.session.add(new_entry)

    if players:
        for player in players:
            db.session.delete(player)
            db.session.commit()

    for player in stats.players:
        if player.games:    
            new_entry = Player(tid, player.id, player.name, player.position, player.games, player.ab, 
                player.hits, player.avg, player.singles, player.doubles, player.triples, player.hr, player.rbi, 
                player.so, player.era, player.slg)
            db.session.add(new_entry)

    if pitchers:
        for player in pitchers:
            db.session.delete(player)
            db.session.commit()
    for player in stats.pitchers:
        if player.era != "-":
            new_entry = Pitcher(tid, player.id, player.name, player.games, player.so, player.era)
            db.session.add(new_entry)
    db.session.commit()

    return render_template('stats.html', stats=stats)

@app.route('/leaders')
def leaders():
    teams = Team.query.filter(Team.games >= 5)
    players = Player.query.filter(Player.games >= 5)
    pitchers = Pitcher.query.filter(Pitcher.games >= 5)

    return render_template('leaders.html', teams=teams, players=players, pitchers=pitchers)

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
